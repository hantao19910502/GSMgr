#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import MySQLdb
import commands
import json
import os
import paramiko
import sys
import urllib
import time
import shutil
from backend.conf import open
from backend.lib import logger
from backend.module.creategame.base.BaseCreateGame import CreateGame
from backend.module.creategame.utils.modify_gsc import modify_gsc
from backend.module.creategame.utils.local_cmd import local_cmd
from backend.module.creategame.utils.scp_dir import scp_dir
from backend.module.creategame.utils.ssh_return import ssh_return
from backend.module.creategame.utils.sanguo_cmd import *
from backend.lib  import accesses
from backend.lib  import mysql
from backend.lib.ssh import *
from library import create_game_tools, GenerateGignature, AccessUrl  
basedir = os.path.abspath(__file__)
basedir = os.path.dirname(basedir)
basedir = os.path.dirname(basedir)

class CPPFramework(CreateGame):
    def __init__(self):

        # gsmgr api set
        self.SERVER_RECORD_API = open.SERVER_RECORD_API
        self.TASK_STATUS_API = open.TASK_STATUS_API
        self.HOSTGROUP_INFO = open.HOSTGROUP_INFO
        self.LOG_FILE = open.LOG_FILE

        # open for each game project
        self.DBROLE_INDEX = "DB"
        self.MAINROLE_INDEX = "MAIN"
        self.LOGICROLE_INDEX = "LOGIC"
        self.PROJ_BASE_CONFIG = None
        self.PROJ_SPECIAL_CONFIG = None
        self.SANGUO_CMD = None

        # web api set
        self.OPEN_GAME_INFO = None
        self.OPEN_GAME_INFO_SECRET = None
        # rolling api set
        self.IP_LIST_API = open.IP_LIST_API
        self.SERVICE_LIST_API = open.SERVICE_LIST_API

        # mysql set
        self.MYSQL_USER = None
        self.MYSQL_PASS = None
        self.MYSQL_ROOT_USER = None
        self.MYSQL_ROOT_PASS = None

        # local params
        self.TaskId = None
        self.Project = None
        self.Hostgroup = None
        self.ServerIds = None

        # global variable
        self.ServerData = {}
        self.SdbHostList = []
        self.MainHostList = []
        self.LogicHostList = []
        self.TmpdbHostList = []
        self.MainGamesCount = []

        # local path
        self.local_lcserver_path = os.path.join(basedir,'tmp','lcserver')
        self.local_rpcfw_path = os.path.join(basedir,'tmp','rpcfw')

	#self.LogicHostList={"sg2.apple":[ip,ip1]}
	#		   {"sg2.android":[ip,ip1]}

	#self.GroupbaseRole={"70000":"sg2.apple"}
	#                    "80000":"sg2.apple"   
	#                    "90000":"sg2.android"   

	self.GroupbaseRole={}
        self.a={}
        self.b={}
    def _get_mdb(self, sdb_ip):

        conn = MySQLdb.connect(host=sdb_ip, user=self.MYSQL_USER, passwd=self.MYSQL_PASS, port=3306)
        cur = conn.cursor()
        slave_status_cur = cur.execute('show slave status')
        slave_status = cur.fetchone()
        columns = cur.description
        tmp = {}
        for (index, column) in enumerate(slave_status):
            tmp[columns[index][0]] = column
        cur.close
        conn.close()
        return tmp['Master_Host']

    def _getpiratedb(self, sdb_list):

        self. ret = []
        for ip in sdb_list:
            sql = "show databases like \'pirate%\'"
            status, db_count = create_game_tools('mysqlconn', ip, 3306, self.MYSQL_USER, self.MYSQL_PASS, sql)
            if status:
                if len(db_count) < self.PROJ_BASE_CONFIG["DatabaseMax"]:
                    self.ret.append({'mdbhost': self._get_mdb(ip), 'sdbhost': ip, 'count': len(db_count)})
            else:
                print "Mysql Error %d: %s" % (db_count.args[0], db_count.args[1])
        return self.ret

    def get_groupbase(self, serverid):
        self.groupbase = ""
        try:
            self.groupbase = str(int(serverid) - (int(serverid) % 100))
            assert len(self.groupbase) == len(str(serverid))
        except Exception, e:
            return None
        return self.groupbase

    # 取字典列表里'count'值最小的一个元素
    def get_min_item(self, dict_list):

        tmp = float('inf')
        d = {}
        x = ""

        try:

            for index, item in enumerate(dict_list):
                if tmp > int(item['count']):
                    tmp = int(item['count'])
                    d = item
                    x = index

        except Exception, e:
            return x, e

        return x, d

    # 取某数据库机器所有tmp库
    def get_tmpdbs(self, ip):
        tmpdbs = []

        try:
            conn = MySQLdb.connect(host=ip, user=self.MYSQL_USER, passwd=self.MYSQL_PASS, port=3306)
            cur = conn.cursor()
            tmpdb = cur.execute('show databases like "tmp%"')
            fetch = cur.fetchmany(tmpdb)
            tmpdbs = [i[0] for i in fetch]

            cur.close()
            conn.close()

        except Exception, e:
            print e
            return tmpdbs

        return tmpdbs

    # 获取所有main机器开服个数
    def get_main_game_count(self, mainhost):

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(mainhost, 22, 'pirate', "")
            stdin, stdout, stderr = ssh.exec_command("ls /home/pirate/lcserver/conf | egrep *.args$ | wc -l")
        except:
            return False, ""

        return True, stdout.read().strip('\n')

    # 获取主机组配置信息
    #def get_hostgroup_info(self, project, hostgroup):
    #    data = {}

    #    parmas = urllib.urlencode({'hostproj': project, 'hostgroup': hostgroup})
    #    f = urllib.urlopen(self.HOSTGROUP_INFO, parmas)

    #    try:
    #        for db in json.loads(f.read()):
    #            data[db[0]] = db[1]
    #    except ValueError, e:
    #        return {}

    #    return data


    def get_groupbase_role(self,serverid):

        url = "http://192.168.1.144:8080/api/role/getrolebygroupbase/?groupbase=%s&project=%s"%(self.get_groupbase(serverid[0]),self.Project)

        #GroupPlat = urllib.urlopen(url).read()

        GroupPlat = {'role':'test.sanguo'}

        self.GroupbaseRole = {self.get_groupbase(self.ServerIds[0][0]):GroupPlat['role']}


        return self.GroupbaseRole

    def get_hostgroup_info(self,serverid,role):

        parmas = self.get_groupbase_role(serverid)


        parmas = parmas[self.groupbase]

        param =  parmas +"."+role

        return param
    # 获取sdb列表
    def get_sdb_list(self,project, hostgroup):

        data = []

        hostgroup_info = self.get_hostgroup_info(project, hostgroup)

        if not hostgroup_info:
            return data

        role = hostgroup_info[self.DBROLE_INDEX]

        services_info = self.get_service_info(role)

        if not services_info:
            return data

        for h in services_info:
            if h['role'].endswith('sdb') and 'sdb' in str(h['host']):
                data.append(h['ipaddr'])

        return data

    # 获取main机器列表
    def get_main_list(self, project, hostgroup):
        data = []
        hostgroup_info = self.get_hostgroup_info(project, hostgroup)
        if not hostgroup_info:
            return data

        role = hostgroup_info[self.MAINROLE_INDEX]

        services_info = self.get_service_info(role)
        if not services_info:
            return data

        for h in services_info:
            if h['role'].endswith('lcserver') and 'main' in str(h['host']):
                data.append(h['ipaddr'])

        return data

    # 获取某新服开服信息
    def get_game_info(self, serverid):
        #url = self.OPEN_GAME_INFO + "?"
	#url = self.PROJ_BASE_CONFIG[self.Project]['GameInfoUrl']
	url ="http://192.168.1.38/stat/getserverinfo/getInfoByOneServer?"
        time_stamp = str(time.time()).split('.')[0]

        dic = {'groupid': serverid[0], 'tm': time_stamp, 'lid': serverid[1]}
        sign = GenerateGignature().get_sign(dic, self.PROJ_BASE_CONFIG[self.Project]['Secret'] )
        dic['sign'] = sign

        url += str(urllib.urlencode(dic))
        sv_info = {}
        try:
            gm = AccessUrl().get_url(url)['info'][0]
            time_local = time.localtime(gm['openDateTime'])
            dt = time.strftime("%Y%m%d", time_local)
            tm = time.strftime("%H%M00", time_local)

            sv_info = {'gameid': gm['groupid'], 'opendate': dt, 'opentime': tm, 'servername': gm['name'],
                       'sid': gm['sid'], 'iscallback': ''}
        except Exception, e:
            return {}
        return sv_info

    # 取开服外网端口
    def get_wanport(self, sid, serverid):

	print 'get_groupbase:',self.get_groupbase(serverid[0])
        wanport = int(sid) + int(self.sanguo_base_config[self.get_groupbase(serverid[0])]["WanBasePort"])
        return wanport

    # 取开服内网端口
    def get_lanport(self, sid, serverid):

        lanport = int(sid) + int(self.sanguo_base_config[self.get_groupbase(serverid[0])]["LanBasePort"])
        return lanport

    # 获取logic机器列表
    def get_logiclist(self, project, hostgroup):
        data = []
        hostgroup_info = self.get_hostgroup_info(project, hostgroup)
        if not hostgroup_info:
            return data
        role = hostgroup_info[self.LOGICROLE_INDEX]

        services_info = self.get_service_info(role)
        if not services_info:
            return data

        for h in services_info:

            if h['role'].endswith('phpproxy') and 'logic' in str(h['host']):
                data.append(h['ipaddr'])

        return data

    # 取boss战偏移量
    def get_offset(self, mainhost):

        file_name =  basedir +'/cache/' + mainhost
        offset_list = self.sanguo_base_config['BossOffset']

        offset = 0
        if os.path.exists(file_name):
            f = file(file_name, 'r')
            offset = str(f.read())
            f.close()
        offset = int(offset)
        offset += 1
        if offset > 3:
            offset = 0
        f = file(file_name, 'w')
        f.write(str(offset))
        f.close()

        return offset_list[offset]

    # 选一个main机器
    def choice_main(self, main_count):

        k, v = self.get_min_item(main_count)
        num = int(v['count'])
        num += 1

        main_count[k]['count'] = num
        return str(v['mainhost'])

    # 统计数据库个数,及tmp库列表
    def count_dbhost_tmpdb(self, sdb_list):

        dbgroup_tmpdb_list = []

        dbgroup_list = self._getpiratedb(sdb_list)
        if not dbgroup_list:
            return []

        for i in dbgroup_list:

            tmpdb = self.get_tmpdbs(i['sdbhost'])

            if tmpdb:
                tmp = {"mdbhost": i["mdbhost"], "sdbhost": i["sdbhost"], "count": i['count'], "tmpdblist": tmpdb}
                dbgroup_tmpdb_list.append(tmp)
        return dbgroup_tmpdb_list

    # 选一组有可用tmp库的数据库机器
    def choice_tmpdb(self, db_count_list):

        k, v = self.get_min_item(db_count_list)

        num = int(v['count'])
        num += 1

        db_count_list[k]['count'] = num
        tmpdb = {'mdbhost': v['mdbhost'], 'sdbhost': v['sdbhost'], 'tmpdb': v['tmpdblist'][0]}

        del db_count_list[k]['tmpdblist'][0]

        if not db_count_list[k]['tmpdblist']:
            del db_count_list[k]

        return tmpdb

    # 生成args
    def gen_args(self, serverid, lanport, wanport, Hostgroup):
        print "gen_args"
        zkpath = self.PROJ_SPECIAL_CONFIG[Hostgroup]['LogicZKPath']

        argsname = 'game' + serverid + '.args'        
        argspath = os.path.join(self.local_lcserver_path, argsname)

        if not os.path.exists(argspath):
            f = file(argspath, 'w')
            f.write(self.PROJ_SPECIAL_CONFIG['WriteArgs'] %(serverid, lanport, wanport, zkpath))
            f.close()
            return True


    # 生成gsc
    def gen_gsc(self, serverid, opendate, opentime, offset):
        print "gen_gsc"

        rpcfwname = 'game' + serverid
        rpcfwpath = os.path.join(self.local_rpcfw_path, rpcfwname)

        if not os.path.isdir(rpcfwpath):
            shutil.copytree(self.PROJ_SPECIAL_CONFIG['TemplatePath'], rpcfwpath)
            modify_gsc(opendate, opentime, offset, rpcfwpath)
            return True


    # 重命名数据库
    def rename_db(self, serverid, mdbhost, tmpdb, MYSQL_ROOT_USER, MYSQL_ROOT_PASS):
        print "rename_db"

        if not ssh_return(mdbhost, self.SANGUO_CMD.rename_exists, "1"):
            return False
        if not ssh_return(mdbhost, self.SANGUO_CMD.rename_cmd %(MYSQL_ROOT_USER, MYSQL_ROOT_PASS, tmpdb, serverid), "done"):
            return False
        return True

    # 拷贝args到main机器
    def copy_args(self, serverid, mainhost):
        print "copy_args"

        argsname = 'game' + serverid + '.args'
        argspath = os.path.join(self.local_lcserver_path, argsname)

        if not ssh_return(mainhost, self.SANGUO_CMD.args_exists %(self.PROJ_SPECIAL_CONFIG['LCConf'], serverid), "0"):
            return False
        scp(mainhost, argspath, os.path.join(self.PROJ_SPECIAL_CONFIG['LCConf'], argsname))
        return True

    # 拷贝gsc到main机器
    def copy_gsc(self, serverid, mainhost):
        print "copy_gsc"

        rpcfwname = 'game' + serverid
        rpcfwpath = os.path.join(self.local_rpcfw_path, rpcfwname)
        torpcfwpath = os.path.join(self.PROJ_SPECIAL_CONFIG['RPCConf'],rpcfwname)

        if not ssh_return(mainhost, self.SANGUO_CMD.gsc_exists %(self.PROJ_SPECIAL_CONFIG['RPCConf'], serverid), "0"):
            return False
        scp_dir(mainhost, rpcfwpath, torpcfwpath)
        return True



    # 拷贝gsc到logic机器
    def copy_gsc_to_logic(self, serverid, logichostlist):
        print "copy_gsc_to_logic"

        rpcfwname = 'game' + serverid
        rpcfwpath = os.path.join(self.local_rpcfw_path, rpcfwname)
        torpcfwpath = os.path.join(self.PROJ_SPECIAL_CONFIG['RPCConf'],rpcfwname)
        issuccess = True
        faillist = []

        try:
            for i in logichostlist.values()[0]:
                if not ssh_return(i, self.SANGUO_CMD.gsc_exists %(self.PROJ_SPECIAL_CONFIG['RPCConf'], serverid),"0"):
                    return False
                scp_dir(i, rpcfwpath, torpcfwpath)
            return issuccess, faillist
        except Exception:
            return False

    # 初始化dataproxy配置
    def init_dataproxy(self, serverid, sdbhost):
        print "init_dataproxy"

        if not ssh_return(sdbhost, self.SANGUO_CMD.dataproxy_exists %(self.PROJ_SPECIAL_CONFIG['DataproxyPath'], serverid), "0"):
            return False

        a,b = cmd(sdbhost, self.SANGUO_CMD.dataproxy_cmd %(self.PROJ_SPECIAL_CONFIG['DataproxyPath'], serverid))
        #status = a.strip("\n")
        if a:
            return True
        else:
            return False

    # 初始化服
    def init_game(self, serverid, mainhost):
        print "init_game"

        if not ssh_return(mainhost, self.SANGUO_CMD.init_exists %(self.PROJ_SPECIAL_CONFIG['InitPath']), "1"):
            return False

        a,b = cmd(mainhost, self.SANGUO_CMD.init_cmd %(self.PROJ_SPECIAL_CONFIG['InitPath'], serverid))
        #output = a.strip("\n")
        if a:
            return True
        else:
            return False

    # 起服
    def start_game(self, serverid, mainhost):
        print "start_game"

        if not ssh_return(mainhost, self.SANGUO_CMD.args_exists %(self.PROJ_SPECIAL_CONFIG['LCConf'], serverid), "1"):
            return False
        if not local_cmd(self.SANGUO_CMD.check_start_cmd %(basedir, mainhost, serverid, self.PROJ_SPECIAL_CONFIG['LCTest'])):
            return False
        return True



    # 检查新开服
    def check_game(self, serverid, mainhost, mdbhost, MYSQL_ROOT_USER, MYSQL_ROOT_PASS):
        print "check_game"

        if not ssh_return(mainhost, self.SANGUO_CMD.init_exists %(self.PROJ_SPECIAL_CONFIG['InitPath']), "1"):
            return False
        a,b = cmd(mainhost, self.SANGUO_CMD.check_init_cmd %(self.PROJ_SPECIAL_CONFIG['InitPath'], serverid), 'pirate')
        output = b.strip("\n")
        if not output:
            return True
        else:
            return False

    # 统计所有main机器开服个数
    def count_main_games(self, mainhostlist):
        count_main = []
        for i in mainhostlist:
            k, v = self.get_main_game_count(i)
            if not k:
                logger.Logger("warn", "CreateGameSanguo.count_main_games", "get mainhost games count faild!")
                continue

            if int(v) < int(self.PROJ_BASE_CONFIG["LcserverMax"]):
                count_main.append({"mainhost": i, "count": v})

        return count_main

    def cpp_before(self):
        ost = OpenServerTask.objects.get(id=self.TaskId)
        if ost.status != 1 and ost.status != 5:
            sys.exit()
 
	self.SdbHostList = self.get_sdb_list(self.Project ,self.Hostgroup)
	print 'SdbHostList:',self.SdbHostList
        if not self.SdbHostList:
            logger.Logger("error", "CreateGameSanguo.get_sdb_list", "sdb host list is empty!")
            self._post_task_status(self.TaskId, 5, "get sdb host list faild!")
            sys.exit()

        self.MainHostList = self.get_main_list(self.Project ,self.Hostgroup)
        if not self.MainHostList:
            logger.Logger("error", "CreateGameSanguo.get_main_list", "main host list is empty!")
            self._post_task_status(self.TaskId, 5, "get main host list faild!")
            sys.exit()

        self.LogicHostList = self.get_logiclist(self.Project, self.Hostgroup)
        if not self.LogicHostList:
            logger.Logger("error", "CreateGameSanguo.before", "get_logiclist")
            self._post_task_status(self.TaskId, 5, "get logic host list faild!")
            sys.exit()

        for serverid  in self.ServerIds:
	     print "serverid:",serverid
             role = self.get_groupbase_role(serverid)

             role = role.values()[0]

             if self.a.keys()  != role:
                self.TmpdbHostList = self.count_dbhost_tmpdb(self.SdbHostList[role+".db"])
                self.a[role] = self.TmpdbHostList
             if not self.TmpdbHostList:
                 logger.Logger("error", "CreateGameSanguo.count_dbhost_tmpdb", "tmpdb host list is empty!")
                 self._post_task_status(self.TaskId, 5, "get tmpdb host faild!")
                 sys.exit()
             
             if self.b.keys() != role:
                 self.MainGamesCount = self.count_main_games(self.MainHostList[role+".main.lcserver"])
                 self.b[role] = self.MainGamesCount

             if not self.MainGamesCount:
                 logger.Logger("error", "CreateGameSanguo.count_main_games", "get available main host faild!")
                 self._post_task_status(self.TaskId, 5, "get available main host list faild!")
                 sys.exit()
             
             
             tmpsum = 0
            # for h in self.TmpdbHostList:
            #     tmpsum += len(h['tmpdblist'])

            # if tmpsum < len(self.ServerIds):
            #     logger.Logger("error", "CreateGameSanguo.before", " %s tmpdb not enough!" % str(self.TaskId))
            #     self._post_task_status(self.TaskId, 5, "tmpdb count:%s not enough" % str(tmpsum))
            #     sys.exit()

             availablesum = 0
             for h in self.MainGamesCount:
                 num = int(self.PROJ_BASE_CONFIG['LcserverMax']) - int(h['count'])
                 availablesum += num

             groupbase = self.get_groupbase(serverid[0])
             game_info = self.get_game_info(serverid)
	     print 'game_info:',game_info
             tmpdb_info = self.choice_tmpdb(self.a[role])
             mainhost = self.choice_main(self.b[role])
             wanport = self.get_wanport(game_info['sid'], serverid)
             lanport = self.get_lanport(game_info['sid'], serverid)
             offset = self.get_offset(mainhost)



             data = {
                 'status': 'success',
                 'failoutput': "",
                 "mainhost": mainhost,
                 "mdbhost": tmpdb_info['mdbhost'],
                 "sdbhost": tmpdb_info['sdbhost'],
                 "tmpdb": tmpdb_info['tmpdb'],
                 'opendate': game_info['opendate'],
                 'opentime': game_info['opentime'],
                 'gameid': game_info['gameid'],
                 'iscallback': game_info['iscallback'],
                 'servername': game_info['servername'],
                 'sid': game_info['sid'],
                 'wanport': wanport,
                 'lanport': lanport,
                 'offset': offset,
                 'lid': serverid[0],
		 'groupbase':groupbase
             }

             self.ServerData[str(serverid[0])] = data
	logger.Logger('info','ServerData',self.ServerData)


        return self.ServerData 
    def cpp_create(self):
        for server, info in self.ServerData.items():

            if not self.rename_db(server, info['mdbhost'], info['tmpdb'], self.MYSQL_ROOT_USER, self.MYSQL_ROOT_PASS):
                self.ServerData[server]['status'] = 'faild'
                self.ServerData[server]['failoutput'] = "rename database faild"
                logger.Logger("error", "CreateGameSanguo.rename_db", " server:%s mdb:%s tmpdb:%s faild" %
                              (server, info['mdbhost'], info['tmpdb']))
                continue

            if not self.gen_args(server, info['lanport'], info['wanport'], info['groupbase']):
                 self.ServerData[server]['status'] = 'faild'
                 self.ServerData[server]['failoutput'] = "generate lcserver args faild"
                 logger.Logger("error", "CreateGameSanguo.gen_args", "server:%s generate args faild!" % server)
                 continue

            if not self.gen_gsc(server, info['opendate'], info['opentime'], info['offset']):
                self.ServerData[server]['status'] = 'faild'
                self.ServerData[server]['failoutput'] = "generate rpcfw gsc faild"
                logger.Logger("error", "CreateGameSanguo.gen_gsc", "server:%s generate gsc faild!" % server)
                continue

            if not self.copy_args(server, info['mainhost']):
                self.ServerData[server]['status'] = 'faild'
                self.ServerData[server]['failoutput'] = "copy args to mainhost faild"
                logger.Logger("error", "CreateGameSanguo.copy_args", "server:%s copy args to mainhost:%s faild" %
                              (server, info['mainhost']))
                continue

            if not self.copy_gsc(server, info['mainhost']):
                self.ServerData[server]['status'] = 'faild'
                self.ServerData[server]['failoutput'] = "copy gsc to mainhost faild"
                logger.Logger("error", "CreateGameSanguo.copy_gsc", "server:%s copy gsc to mainhost:%s faild!" %
                              (server, info['mainhost']))
                continue

            if not self.init_dataproxy(server, info['sdbhost']):
                self.ServerData[server]['status'] = 'faild'
                self.ServerData[server]['failoutput'] = "initialize dataproxy data faild"
                logger.Logger("error", "CreateGameSanguo.init_dataproxy", "server:%s init dataproxy data faild!" %
                              server)
                continue

            print self.LogicHostList
            issuccess, output = self.copy_gsc_to_logic(server, self.LogicHostList)
            print self.LogicHostList
            print type(issuccess)
            print issuccess
            if not issuccess:
                self.ServerData[server]['status'] = 'faild'
                self.ServerData[server]['failoutput'] = "copy gsc to logic host faild"
                logger.Logger("error", "CreateGameSanguo.copy_gsc_to_logic",
                              "copy gsc to logichost faild, 'fail': %s." %
                              output)
                continue

    def cpp_after(self):
        for server, info in self.ServerData.items():

            if info['status'] == 'success':

                if not self.start_game(server, info['mainhost']):
                    self.ServerData[server]['status'] = 'faild'
                    self.ServerData[server]['failoutput'] = "start server data faild"
                    logger.Logger("error", "CreateGameSanguo.start_game", "server:%s start faild!" % server)


                if not self.init_game(server, info['mainhost']):
                    self.ServerData[server]['status'] = 'faild'
                    self.ServerData[server]['failoutput'] = "initialize server data faild"
                    logger.Logger("error", "CreateGameSanguo.init_game", "server:%s init game faild!" % server)


                if not self.check_game(server, info['mainhost'], info['mdbhost'], self.MYSQL_USER, self.MYSQL_PASS):
                    self.ServerData[server]['status'] = 'faild'
                    self.ServerData[server]['failoutput'] = "check game faild"
                    logger.Logger("error", "CreateGameSanguo.check_game", "server:%s check game faild!" % server)


            status = 0
            if info['status'] == 'success':
                status = 1
            else:
                status = 2

            extra_data = {
                'failoutput': info['failoutput'],
                "mdbhost": info['mdbhost'],
                "sdbhost": info['sdbhost'],
                "tmpdb": info['tmpdb'],
                'opendate': info['opendate'],
                'opentime': info['opentime'],
                'gameid': info['gameid'],
                'iscallback': info['iscallback'],
                'servername': info['servername'],
                'wanport': info['wanport'],
                'lanport': info['lanport'],
                'offset': info['offset'],
            }
	    #print 'groupbase',self.get_groupbase(server)
	    #print 'pingtai',self.get_groupbase_role(server)[self.get_groupbase(server)].split(".")[1]
            dt = info['opendate']
            dt1 = dt[:4] + "-" + dt[4:6] + "-" + dt[6:8]            
            tm = info['opentime']
            tm1 = tm[:2] + ":" + tm[2:4] + ":" + tm[4:6]


            self._record_server_info(server, dt1, tm1, info['mainhost'], self.Project, extra_data, status)

        status = 0
        mess = ""
        for server, info in self.ServerData.items():
            if info['status'] == 'faild':
                status = 1
                mess += "[" + server + "]"
	print 'status:',status
        if status != 0:
            self._post_task_status(self.TaskId, 3, mess)
        else:
            self._post_task_status(self.TaskId, 4, "success")

