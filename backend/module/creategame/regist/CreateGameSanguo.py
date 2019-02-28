#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys,os,paramiko
sys.path.append('/home/pirate/django/GSMgr')
from backend.module.creategame.base.BaseCreateGame import CreateGame
from backend.module.creategame.frame.CPPFramework import CPPFramework
sys.path.append('/home/pirate/django/GSMgr/backend/module/creategame/conf')
import sanguo_config
from backend.lib import logger
from backend.conf import open
from backend.module.creategame.utils import sanguo_cmd
 


class CreateGameSanguo(CPPFramework):

    def __init__(self,*args):
        super(CreateGameSanguo,self).__init__()

        #rewrite CPPFramework
        self.PROJ_BASE_CONFIG = open.GAME_PROJ_INFO
        self.IP_LIST_API = open.IP_LIST_API
        self.MYSQL_USER = open.MYSQL_USER
        self.MYSQL_PASS = open.MYSQL_PASS
        self.MYSQL_ROOT_USER = open.MYSQL_ROOT_USER
        self.MYSQL_ROOT_PASS = open.MYSQL_ROOT_PASS
        self.PROJ_SPECIAL_CONFIG = sanguo_config.BASE_CONFIG
	self.sanguo_base_config = sanguo_config.BASE_CONFIG
        self.SANGUO_CMD = sanguo_cmd 

        #local params
        self.TaskId = args[0]
        self.Project = args[1]
        self.ServerIds = args[2]
	
	self.dbgroup_tmpdb_list = []
    def test(self):
        print self.TaskId
	print self.Project
	print self.ServerIds


    def before(self):
	print self.cpp_before()	
        #self.cpp_before()

    def create(self):
        #pass
        self.cpp_create()

    def after(self):
        #pass
        self.cpp_after()

    def get_sdb_list(self,project,hostgroup):
        
        data = []

        #role = hostgroup_info[self.DBROLE_INDEX]
        for  serverid in self.ServerIds: 

             role = self.get_hostgroup_info(serverid,'db')
              
             services_info = self.get_service_info(role)
             
             if not services_info:
                 return data

             for h in services_info:
                 if h['role'].endswith('sdb') and 'test' in str(h['host']):
                     data.append({role:h['ipaddr']})
             dic = {}
             for _ in data:
                 for k, v in _.items():
                     dic.setdefault(k, []).append(str(v))

        data = [{k:v} for k, v in dic.items()]
        dic1 = {}
        for h in data:
            dic1.update(h)
        va = list(set(dic1.values()[0]))
        ke = dic1.keys()[0]
        return {ke:va}

    def get_main_list(self,project,hostgroup):
    
        data = []
         
        #role = hostgroup_info[self.DBROLE_INDEX]
        for  serverid in self.ServerIds: 
        
             role = self.get_hostgroup_info(serverid,'main.lcserver')
              
             services_info = self.get_service_info(role)
             
             if not services_info:
                 return data
                 
             for h in services_info:
                 if h['role'].endswith('lcserver') and 'test' in str(h['host']):
                     data.append({role:h['ipaddr']})
             dic = {}
             for _ in data:
                 for k, v in _.items():
                     dic.setdefault(k, []).append(str(v))
                     
        data = [{k:v} for k, v in dic.items()]
        dic1 = {}
        for h in data:
            dic1.update(h)
        va = list(set(dic1.values()[0]))
        ke = dic1.keys()[0]
        return {ke:va}

    def get_logiclist(self,project,hostgroup):
        data = []

        #role = hostgroup_info[self.DBROLE_INDEX]
        for  serverid in self.ServerIds:

             role = self.get_hostgroup_info(serverid,'logic.phpproxy')

             services_info = self.get_service_info(role)

             if not services_info:
                 return data

             for h in services_info:
                 if h['role'].endswith('phpproxy') and 'test' in str(h['host']):
                     data.append({role:h['ipaddr']})
             dic = {}
             for _ in data:
                 for k, v in _.items():
                     dic.setdefault(k, []).append(str(v))

        data = [{k:v} for k, v in dic.items()]
        dic1 = {}
        for h in data:
            dic1.update(h)
        va = list(set(dic1.values()[0]))
        ke = dic1.keys()[0]
        return {ke:va}


    def NetCheck(self,ip):
          p = subprocess.Popen(["ping -c 1 -w 1 "+ ip],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
          out=p.stdout.read()
          regex=re.compile('100% packet loss')
          if len(regex.findall(out)) == 0:
              return True 
          else:
              return False

    def check_db_exit(self, ip,db):
         conn = MySQLdb.connect(host=ip, user="root", passwd="", port=3306)
         cur = conn.cursor()
         tmpdb = cur.execute('show databases like "%s%%"'%(dbname))
         fetch = cur.fetchmany(tmpdb)
         cur.close()
         conn.close()
         return tmpdb

    def check_network(self):
        flag = True
        all_list = []
        print self.SdbHostList
        all_list +=self.SdbHostList
        all_list +=self.MainHostList
        print all_list
        for ip in  all_list:
            if not self.NetCheck(ip):
    
                flag = False
            else:
                flag = True
        return flag

    def check_exit_main(self,ip,gameid):
                flag = False
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip, 22, 'pirate', "")
                    stdin, stdout, stderr = ssh.exec_command("ls /home/pirate/lcserver/conf | egrep %s | wc -l"%(gameid))
                except Exception, e:
                    print e
                    flag = True

                if int(stdout.read().strip('\n')) is  0:
                        flag =  True
                        

                return flag, stdout.read().strip('\n')


    def check_exit_db(self,ip,gameid):
            flag = False
            try:
                  conn = MySQLdb.connect(host=ip, user=self.MYSQL_USER, passwd=self.MYSQL_PASS, port=3306)
                  cur = conn.cursor()
                  piratedb = cur.execute('show databases like "pirate%s"'%(gameid))
                  fetch = cur.fetchmany(piratedb)

                  cur.close()
                  conn.close()

            except Exception, e:
                  print e
                  flag =  True
            if not fetch:
                  flag = True

            if  list(fetch)[0][0] is 0:
                   flag = True


            return flag

    def check_env(self):
        #check run script env
        # return True/False
        return True

    def check_exits(self,gameid):
        # pirate20001 9.192
        # game20001.args
        # check the server exists that will be created
        # check the dbname exists that will be created

        flag = True
        for main_ip in self.MainHostList:

            if  self.check_exit_main(main_ip,gameid):

                print "exit main"

                flag =  False

        for db_ip in self.sdbHostList:

            if self.check_exit_db(db_ip,gameid):

               print "exit piratedb"

               flag =  False

        return flag

    def count_dbhost_tmpdb(self, sdb_list):

    	if not self.dbgroup_tmpdb_list:

    	    dbgroup_list = self._getpiratedb(sdb_list)
    	    if not dbgroup_list:
    	        return []

    	    for i in dbgroup_list:

    	        tmpdb = self.get_tmpdbs(i['sdbhost'])

    	        if tmpdb:
    	            tmp = {"mdbhost": i["mdbhost"], "sdbhost": i["sdbhost"], "count": i['count'], "tmpdblist": tmpdb}
    	            self.dbgroup_tmpdb_list.append(tmp)
    	return self.dbgroup_tmpdb_list

#if __name__ == "__main__":
#    a = CreateGameSanguo(12,'test',[(70001,73),(70002,73)])
##    a = CreateGameSanguo(12,'test',[(70001,73),(70002,73)])
#    a.before()
#    a.create()
#    a.after()
