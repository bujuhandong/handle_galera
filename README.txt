# MySQL galera 节点添加、节点删除、MGR状态检查、数据库起停工具
程序名：handle_galera

### 程序结构：
```
handle_galera/
|-- bin/
|   |-- __init__.py
|   |-- handle_galera.py
|
|-- core/
|   |-- __init__.py
|   |-- main.py  
|-- conf/
|   |-- galera.conf   ##handle_galera配置文件
|   |-- example_galera.conf  ##参考配置文件
|-- README

```

### 运行环境：
    Python3.0或以上版本环境均可。


### 执行方法：
    python3 handle_galera.py
	
### 使用方法：
    1) 编辑配置文件conf/galera.conf，以下为配置文件参数解析:
	  ####[default]必须存在，放MySQL的一些相关信息，包括defaults-file、datadir、basedir、
	  ####user、password、socket几个参数
      ####用户可以根据实际情况更改。其中datadir必须运行前已存在。
      [default]
      defaults-file = /57data/galera_my/my.cnf
      datadir = /57data/galera_my
      basedir = /usr/local/mysql215
      user = root
      password = mysql
      socket = /tmp/mysql3307.sock
      
      
      ###########以下为MySQL配置文件中需要存的内容##############
      [client]
      default-character-set = utf8
      port = 3307
      
      [mysql]
      default-character-set = utf8
      
      
      [mysqld]
      basedir = /usr/local/mysql215
      datadir = /57data/galera_my
      socket = /tmp/mysql3307.sock
      user = mysql
      character-set-server = utf8
      collation-server = utf8_general_ci
      port = 3307
      server-id = 3
      
      
      binlog_format=ROW
      default_storage_engine=innodb
      innodb_autoinc_lock_mode=2
      innodb_flush_log_at_trx_commit=0
      innodb_buffer_pool_size=122M
      
      #########以下wsrep_开头参数为galera相关配置信息#######################
      wsrep_provider=/usr/local/mysql215/lib/plugin/libgalera_smm.so
      wsrep_provider_options="gcache.size=300M; gcache.page_size=300M"
      wsrep_cluster_name="example_cluster"
      wsrep_cluster_address="gcomm://10.0.0.13"
      
      ##########以下wsrep_sst_开头参数和[sst]部分为添加新节点是必须存在的信息##################
      wsrep_sst_method=xtrabackup
      wsrep_sst_donor = vm3
      wsrep_sst_auth = sstuser:mysql
      
      [sst]
      streamfmt=xbstream
      
	  
    2) 根据系统提示输入需要的操作类型。
	    1:'Check the galera status',
        2:'Add new galera node',
        3:'Delete galera node',
        4:'Start MySQL instance',
        5:'Stop MySQL instance',
        6:'Exit'

