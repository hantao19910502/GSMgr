#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys, os, paramiko, json
import threading
from backend.module.mergegame.utils.MergeThread import MergeThread
from backend.conf import merge
from backend.lib import accesses
from backend.module.mergegame.utils.CheckDbs import CheckDbs
from backend.utils.taskinfo import BaseUtils


class MutilMergeGame(BaseUtils):
    def __init__(self):
        super(MutilMergeGame, self).__init__()

        self.TaskId = None
        self.Project = None
        self.TargetId = None
        self.Retry = False

        # global configure
        self.ROLE_BY_GROUPBASE_API = merge.ROLE_BY_GROUPBASE_API
        self.IP_LIST_API = merge.IP_LIST_API
        self.SERVICE_LIST_API = merge.SERVICE_LIST_API
        self.GAME_PROJ_INFO = merge.GAME_PROJ_INFO

        # rewrite
        self.BASE_CONFIG = None

        self.SERVER_SET_API = merge.SERVER_SET_API
        self.SERVER_STATUS_SET_API = merge.SERVER_STATUS_SET_API

        # local var
        self.MergeData = []

        self.DBHosts = {}
        self.MatchGroupBaseRole = {}

        # system config
        self.sysuser = None
        self.syspasswd = None
        self.mergehost = None
        self.mergescript = None
        self.procnum = None
        self.sshmode = None
        self.sshpkey = None
        self.tmpdir = None

        # mysql config
        self.user = None
        self.passwd = None

    # 获取字典中key:count最小的项
    def get_min_item(self, dict_list):

        tmp = float('inf')
        d = {}
        x = ""

        for index, item in enumerate(dict_list):
            if tmp > int(item['count']):
                tmp = int(item['count'])
                d = item
                x = index

        return x, d

    def _get_groupbase(self, targetid):

        return targetid.split('_')[0]

    def _get_dblist(self, role):

        url = self.SERVICE_LIST_API + role
        data = accesses.get(url)

        tmplist = []

        for h in data:
            if h['role'].split('.')[-1] == 'sdb':
                tmplist.append({"sdb": h['ipaddr'], "count": None})

        return tmplist

    def _get_rolename(self, groupbase):
        url = self.ROLE_BY_GROUPBASE_API + "groupbase=%s&project=%s" % (str(groupbase), self.Project)
        data = accesses.get(url)

        return data['role']

    def _set_data(self):

        for k, _ in self.DBHosts.items():
            for x, h in enumerate(self.DBHosts[k]):
                c = CheckDbs(h['sdb'], 3306, self.user, self.passwd)
                sum = c.count_dbs('pirate')

                self.DBHosts[k][x]['count'] = sum

    def _distribute_data(self):

        for h in self.TargetId:
            h1 = h.split('.')
            tmp_d = {'targetid': h1[1], 'id': h1[0], 'mdb': '', 'sdb': ''}

            gpb = self._get_groupbase(h1[1])
            roleproj = self.MatchGroupBaseRole[gpb]

            index, dblist = self.get_min_item(self.DBHosts[roleproj])
            self.DBHosts[roleproj][index]['count'] += 10000
            mdb = CheckDbs(self.DBHosts[roleproj][index]['sdb'], 3306, self.user, self.passwd).get_mdb()

            tmp_d['sdb'] = self.DBHosts[roleproj][index]['sdb']
            tmp_d['mdb'] = mdb
            self.MergeData.append(tmp_d)

    def cpp_before(self):

        for i in self.TargetId:
            i1 = i.split('.')
            gpb = self._get_groupbase(i1[1])
            if self.MatchGroupBaseRole.has_key(gpb):
                continue
            roleproj = self._get_rolename(gpb)

            if not roleproj:
                print 'get rolename faild when deal targetid ', i
                return
            self.MatchGroupBaseRole[gpb] = roleproj

            if self.DBHosts.has_key(roleproj):
                continue
            rolename = roleproj + '.' + self.BASE_CONFIG['DB']

            dblist = self._get_dblist(rolename)
            self.DBHosts[roleproj] = dblist

        self._set_data()
        self._distribute_data()

    def cpp_merge(self):

        try:
            self.cpp_before()
        except Exception, e:
            self.setTaskStatus(self.TaskId, 5, "get merge-data")
            print e.__class__, 'Error CPPFramework.MutilMergeGame.cpp_before ', e
            return

        for i in self.MergeData:

            mdbhost = i['mdb']
            sdbhost = i['sdb']
            targetid = i['targetid']
            id = i['id']

            try:
                t = MergeThread(self.TaskId, self.Project, mdbhost, sdbhost, targetid, id)

                t.setExeConf(self.mergehost, self.mergescript, user=self.sysuser, passwd=self.syspasswd, mode=self.sshmode,
                             pkey=self.sshpkey, procnum=self.procnum)

                t.setDaemon(False)
                t.start()
            except Exception, e:
                print "Error CPPframewor.cpp_merge: ", e

    def cpp_retry_merge(self):

        for i in self.MergeData:
            mdbhost = i['mdb']
            sdbhost = i['sdb']
            targetid = i['targetid']
            sid = i['id']

            t = MergeThread(self.TaskId, self.Project, mdbhost, sdbhost, targetid, sid)

            t.setExeConf(self.mergehost, self.mergedir, user=self.sysuser, passwd=self.syspasswd, mode=self.sshmode,
                         pkey=self.sshpkey, procnum=self.procnum, retry=True)

            t.setDaemon(False)
            t.start()