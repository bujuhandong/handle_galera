#!/usr/bin/env  python3
# author: wugong
import os
import sys
BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import main

if __name__ == "__main__":
    conf = BASE_DIR + "/conf/galera.conf"
    status = 0
    action={
        1:'Check the galera status',
        2:'Add new galera node',
        3:'Delete galera node',
        4:'Start MySQL instance',
        5:'Stop MySQL instance',
        6:'Exit'
    }
    while status == 0:
        act_status = 0
        while act_status == 0:
            print("Below is the action list:")
            for i in range(1, 7):
                print(i, ":", action[i])
            act = input("Please select the action number you want:")
            if act.isdigit():
                act = int(act)
                act_status = 1
            else:
                print("\033[31;1mThe input is invalid! Please retry:\033[0m")
                act_status = 0

        if act == 1:
            main.gar_status(conf)
        elif act == 2:
            main.add_members(conf)
        elif act == 3:
            main.del_members(conf)
        elif act == 4:
            main.start_instance(conf)
        elif act == 5:
            main.stop_instance(conf)
        elif act == 6:
            exit("Thanks to use!")
