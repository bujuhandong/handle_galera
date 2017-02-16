#!/usr/bin/env  python3
# author: wugong
import re
import os
import configparser
import shutil
import datetime
import pymysql
import time


def deal_conf(cf_file):  ##根据handle的配置文件生成MySQL配置文件，对原文件做备份
    garconf = configparser.ConfigParser()
    garconf.read(cf_file)
    mysql_cf = garconf['default']['defaults-file']
    with open(mysql_cf, 'w') as f:
        mycf = configparser.ConfigParser()
        mycf.read(mysql_cf)
        secs = garconf.sections()
        for i in secs:
            if i != 'default':
                mycf[i] = garconf[i]
        mycf.write(f)

def start_instance(cf_file):   ##startup mysql instance 启动实例
    config = configparser.ConfigParser()
    config.read(cf_file)
    BASEDIR = config['default']['basedir']
    DEFAU_FILES = config['default']['defaults-file']
    CMD = "cd " + BASEDIR +" ; "+ "bin/mysqld_safe " + " --defaults-file="+ DEFAU_FILES + " &"
    if os.system(CMD):
        print("The instance start failed, Please check the error log!\n")
    else:
        print("The instance started\n")

def stop_instance(cf_file):  ##stop mysql instance 关闭实例
    config = configparser.ConfigParser()
    config.read(cf_file)
    BASEDIR = config['default']['basedir']
    USER = config['default']['user']
    PASS = config['default']['password']
    SOCKET = config['default']['socket']
    CMD = "cd " + BASEDIR +" ; "+ "bin/mysql " + " -u"+USER+" -p"+PASS+" -S"+SOCKET +" -e 'shutdown;'"
    os.system(CMD)
    SOCKETS = config['default']['socket']
    while True:
        os_cmd = "ps -ef |grep " + SOCKETS + " | grep -v grep"
        resp = os.popen(os_cmd).readlines()
        if not resp:
            print("The instance stopped!")
            break
    return 0

def gar_status(cf_file):   ##check the mgr status 检查MGR的状态，组成员、primary site.
    garconf = configparser.RawConfigParser()
    garconf.read(cf_file)
    USER = garconf['default']['user']
    PASS = garconf['default']['password']
    SOCKET = garconf['default']['socket']
    mysqlcon = pymysql.connect(user=USER, password=PASS, unix_socket=SOCKET)
    cur = mysqlcon.cursor()
    def exe_sql(sql_txt):
        cur.execute(sql_txt)
        index = cur.description
        col = []
        for i in index:
            col.append(i[0])
        print("SQL> ",sql_txt)
        print(" ", col[0].ljust(35, ' '), col[1],"\n ", "".center(len(str(col[1]))+50, "-"))
        for i in cur:
            reline = re.findall('^\((.+)\)$', str(i))[0].replace("'", "").split(",")
            print(" ", reline[0].ljust(35, ' '), reline[1])
        print("\n\n")
    sql="show global status like '%wsrep_%'"
    print(sql,"\n")
    exe_sql(sql)
    cur.close()
    mysqlcon.close()

def add_members(cf_file):  ##create user,change master,install plugin,start group_replication
    garconf = configparser.RawConfigParser()
    garconf.read(cf_file)
    DATADIR = garconf['default']['datadir']
    DEFAU_FILES = garconf['default']['defaults-file']
    if os.path.isdir(DATADIR):
        filelist = os.listdir(DATADIR)
        for f in filelist:
            filepath = os.path.join(DATADIR, f)
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath, True)
    deal_conf(cf_file)
    print("Please check the mysql error log for the detail.\n")
    start_instance(cf_file)
    garconf = configparser.RawConfigParser()
    garconf.read(DEFAU_FILES)
    for i in garconf['mysqld']:
        if "wsrep_sst_" in i:
            garconf.remove_option("mysqld", i)
    garconf.write(open(DEFAU_FILES, "w"))

def del_members(cf_file):  ##stop group replication 关闭group replication
    gar_status(cf_file)
    a = stop_instance(cf_file)
    garconf = configparser.RawConfigParser()
    garconf.read(cf_file)
    DEFAU_FILES = garconf['default']['defaults-file']
    SOCKETS = garconf['default']['socket']
    while True:
        os_cmd = "ps -ef |grep " + SOCKETS + " | grep -v grep"
        resp = os.popen(os_cmd).readlines()
        if not resp:
            mynf = configparser.RawConfigParser()
            mynf.read(DEFAU_FILES)
            for i in mynf['mysqld']:
                if "wsrep_" in i:
                    mynf.remove_option("mysqld", i)
            mynf.write(open(DEFAU_FILES, "w"))
            start_instance(cf_file)
            time.sleep(10)
            break
    gar_status(cf_file)


