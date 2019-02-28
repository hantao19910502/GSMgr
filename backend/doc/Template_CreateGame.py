#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys
import MySQLdb
import random
import urllib2
import json
import commands,os
basedir=os.path.abspath(__file__)
basedir=os.path.dirname(basedir)
basedir=os.path.dirname(basedir)
sys.path.append(basedir+"/package")
sys.path.append(basedir+"/config")
from BaseCreateGame import CreateGame
from CPPFramework import CPPFramework
from config import template_config

class  TestCreateGame(CreateGame,CPPFramework):

    def __init__(self,*args):
        # system config
        self.IP_LIST_API = config.IP_LIST_API
        self.SERVER_RECORD_API = config.SERVER_RECORD_API
        self.TASK_STATUS_API = config.TASK_STATUS_API

        # operation config
        self.MYSQL_USER = template_config.MYSQL_USER
        self.MYSQL_PASS = template_config.MYSQL_PASS
        self.DB_MAX_COUNT = template_config.DB_MAX_COUNT
        self.BaseConfig=template_config.BASE_CONFIG

        # parameters
        self.TaskId = args[0]
        self.project = args[1]
        self.platform = args[2]
        self.serverids = args[3]

        # instance varibale
        self.ServerData={}
        self.LogicHostList = []
        self.MainHostList = []
        self.DBHostList = []

    def get_min_count(self,dict_list):

       tmp=float('inf')
       d={}
       x=""

       try:

           for index, item in enumerate(dict_list):
               if tmp > int(item['count']):
                   tmp=int(item['count'])
                   d=item
                   x=index

       except:
           return {}

       return x,d

    def get_db_list(self):
        # get one dbname-mdbhost-sdbhost
        # return True/False
        # put list into self.DBHostList = [[mdb1,sdb1],[mdb2,sdb2]]
        pass

    def get_main_list(self):
        # get one mainhost
        # return True/False
        # put list info self.MainHostList = [main1,main2]
        pass

    def get_game_info(self,serverid):
        # from web api
        # return {'gameid':'','opendate':'','opentime':'','iscallback':'','servername':''}
        pass

    def get_wanport(self,serverid):
        # get lan port
        # return  string  port
        pass

    def get_lanport(self,serverid):
        # get lan port
        # return string port
        pass

    def get_logiclist(self):
        # get logic host list
        # return True/False
        # put list into self.LogicHostList = []
        pass

    def get_offset(self,mainhost):
        # get offset
        # return string offset
        pass

    def choice_main(self):
        # choice one main host
        # return one main ip
        pass

    def choice_sdb(self):
        # choice one sdb host
        # return one {'host':'','tmpdb':''}
        pass

    def gen_args(self,serverid,lanport,wanport):
        # generate lcserver args config
        # return True/False

        pass

    def gen_gsc(self,serverid,opendate,opentime,offset):
        #generate rpcfw gsc
        #  return True/False
        pass

    def rename_db(self,serverid,mdbhost,tmpdb):
        #rename tmpdb to piratedb
        #  return True/False

        pass

    def copy_args(sefl,serverid,mainhost):
        #copy args to main
        # return True/False

        pass

    def copy_gsc(self,serverid,mainhost):
        #copy gsc to main
        # return True/False
        pass

    def copy_gsc_to_logic(self,serverid):
        #copy gsc to logic host
        # return True/False
        pass


    def init_dataproxy(self,serverid,sdbhost):
        #run dataproxy init.sh
        # return True/False

        pass

    def init_game(self,serverid,mainhost):
        #run lcserver init.sh
        # return True/False
        pass

    def start_game(self,serverid,mainhost):
        #start lcserver
        # return True/False
        pass

    def check_game(self,serverid,mainhost):
        #check lcserver init
        # return True/False
        pass

    def check_network(self):
        #check network to host
        # return True/False
        pass

    def check_env(self):
        #check run script env
        # return True/False
        pass
    def check_exsits(self):
        # check if the server exists that will be created
        # check if the dbname exists that will be created
        # return True/False
        pass



    def before(self):

        # _post_task_status
        # 3:任务失败
        # 4:任务完成

        if not self.check_env():
            self._post_task_status(self.TaskId,3,"check env faild!")
            exit()
        if not self.get_db_list():
            self._post_task_status(self.TaskId,3,"get db list faild!")
            exit()
        if not self.get_main_list():
            self._post_task_status(self.TaskId,3,"get main list faild!")
            exit()

        for serverid in self.serverids:
            game_info = self.get_game_info(serverid)
            sdb_info = self.choice_sdb()
            mdb = self._get_mdb(sdb_info['host'])
            main = self.choice_main()
            wanport = self.get_wanport(serverid)
            lanport = self.get_lanport(serverid)
            offset = self.get_offset(main)

            data = {
                'status':'success',
                'failoutput':"",
                "mainhost":main,
                "mdbhost":mdb,
                "sdbhost":sdb_info['host'],
                "tmpdb":sdb_info['tmpdb'],
                'opendate':game_info['opendate'],
                'opentime':game_info['opentime'],
                'gameid':game_info['gameid'],
                'iscallback':game_info['iscallback'],
                'servername':game_info['servername'],
                'wanport':wanport,
                'lanport':lanport,
                'offset':offset,
            }

            self.ServerData[str(serverid)]=data

        if not self.check_network():
            self._post_task_status(self.TaskId,3,"check network faild!")
            exit()

        if not self.check_exsits():
            self._post_task_status(self.TaskId,3,"check exsits faild")
            exit()

        if not self.get_logiclist():
            self._post_task_status(self.TaskId,3,"get logic list faild")
            exit()



    def create(self):

        for server,info in self.ServerData:

            if not self.rename_db(server,info['mdbhost'],info['tmpdb']):
                self.ServerData[server]['status']='faild'
                self.ServerData[server]['failoutput']="rename database faild"
                continue

            if not self.gen_args(server,info['lanport'],info['wanport']):
                self.ServerData[server]['status']='faild'
                self.ServerData[server]['failoutput']="generate lcserver args faild"
                continue

            if not self.gen_gsc(server,info['opendate'],info['opentime'],info['offset']):
                self.ServerData[server]['status']='faild'
                self.ServerData[server]['failoutput']="generate rpcfw gsc faild"
                continue

            if not self.copy_args(server,info['mainhost']):
                self.ServerData[server]['status']='faild'
                self.ServerData[server]['failoutput']="copy args to mainhost faild"
                continue

            if not self.copy_gsc(server,info['mainhost']):
                self.ServerData[server]['status']='faild'
                self.ServerData[server]['failoutput']="copy gsc to mainhost faild"
                continue

            if not self.init_dataproxy(server,info['sdbhost']):
                self.ServerData[server]['status']='faild'
                self.ServerData[server]['failoutput']="initialize dataproxy data faild"
                continue

            if not self.copy_gsc_to_logic(server):
                self.ServerData[server]['status']='faild'
                self.ServerData[server]['failoutput']="copy gsc to logic host faild"
                continue


    def after(self):


        for server,info in self.ServerData:

            if info['status']=='success':

                if not self.init_game(server,info['mainhost']):
                    self.ServerData[server]['status']='faild'
                    self.ServerData[server]['failoutput']="initialize server data faild"
                    continue

                if not self.check_game(server,info['mainhost']):
                    self.ServerData[server]['status']='faild'
                    self.ServerData[server]['failoutput']="check game faild"
                    continue

                if not self.start_game(server,info['mainhost']):
                    self.ServerData[server]['status']='faild'
                    self.ServerData[server]['failoutput']="start server data faild"
                    continue

            status=0
            if info['status'] == 'success':
                status=1
            else:
                status=2

            extra_data = {
                'failoutput':info['failoutput'],
                "mdbhost":info['mdb'],
                "sdbhost":info['sdb'],
                "tmpdb":info['tmpdb'],
                'opendate':info['opendate'],
                'opentime':info['opentime'],
                'gameid':info['gameid'],
                'iscallback':info['iscallback'],
                'servername':info['servername'],
                'wanport':info['wanport'],
                'lanport':info['lanport'],
                'offset':info['offset'],
            }

            self._record_server_info(server,info['opendate'],info['opentime'],info['mainhost'],self.hostproject,self.hostgroup,extra_data,status)

        status = 0
        mess = ""
        for server, info in self.ServerData:
            if info['status'] == 'faild':
                status = 1
                mess += "["+server+"]"

        if status != 0:
            self._post_task_status(self.TaskId, 3, mess)
        else:
            self._post_task_status(self.TaskId, 4, "success")

