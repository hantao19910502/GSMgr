#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys, os, time, urllib
import threading
from backend.lib import ssh
from django.conf import settings
from backend.utils.taskinfo import BaseUtils
from backend.lib import accesses
from backend.conf import merge


class MergeThread(threading.Thread, BaseUtils):
    def __init__(self, *args):
        super(MergeThread, self).__init__()
        BaseUtils.__init__(self)
        self.TaskId = args[0]
        self.project = args[1]
        self.mdbhost = args[2]
        self.sdbhost = args[3]
        self.targetid = args[4]
        self.id = args[5]

        self.TASK_SET_STATUS_API = merge.TASK_STATUS_API
        self.SERVER_SET_API = merge.SERVER_SET_API
        self.SERVER_STATUS_SET_API = merge.SERVER_STATUS_SET_API

    def setExeConf(self, host, mergescript, user=None, passwd=None, mode=None, pkey=None, procnum=1, retry=False):

        self.host = host
        self.mergescript = mergescript
        self.procnum = procnum
        self.mode = mode
        self.pkey = pkey
        self.user = user
        self.passwd = passwd
        self.tmpdir = settings.SCRIPT_CACHE_DIR
        self.retry = retry

    def _run_cmd(self, cmd):
        return ssh.cmd(self.host, cmd, user=self.user, passwd=self.passwd, mode=self.mode, pkey=self.pkey)

    def __run_merge(self):

        if self.retry:

            if open(self.tmpdir + "/" + self.project + ".game" + self.targetid + ".status", 'r').read() == "running":
                return True, {"status": "running"}

            if open(self.tmpdir + "/" + self.project + ".game" + self.targetid + ".status", 'r').read() == "faild":
                cmd = open(self.tmpdir + "/" + self.project + ".game" + self.targetid + ".cmd", 'r').read()
                k, v = self._run_cmd(cmd)
                return k, {"status": "success", "value": v}

            return True, {"status": "success", "value": ""}

        cmd = "%(mergescript)s -d %(mdbhost)s -t %(targetid)s " % {'mergescript': self.mergescript,
                                                                   'mdbhost': self.mdbhost,
                                                                   'targetid': self.targetid}
        if self.procnum > 1:
            cmd += "-m %(procnum)s" % {'procnum': self.procnum}

        with open(self.tmpdir + "/" + self.project + ".game" + self.targetid + ".cmd", "w") as f:
            f.write(cmd)
        f.close()

        with open(self.tmpdir + "/" + self.project + ".game" + self.targetid + ".status", "w") as f:
            f.write('running')
        f.close()

        k, v = self._run_cmd(cmd)
        return k, {"status": "unknow", "value": v}

    def __get_mainhost(self):
        mainhost = "192.168.1.145"
        return mainhost

    def run(self):

        try:
            k, v = self.__run_merge()
        except:
            with open(self.tmpdir + "/" + self.project + ".game" + self.targetid + ".status", "w") as f:
                f.write('running')
            f.close()

        if v['status'] == "running":
            print "Task: %s Group: %s is already in running, ignore... " % (self.TaskId, self.targetid)
            return

        if v['status'] == "success":
            print "Task: #s Group: %s has deal done, ignore..." % (self.TaskId, self.targetid)
            return


        status = 2
        if k:

            with open(self.tmpdir + "/" + self.project + ".game" + self.targetid + ".info", "w") as f:
                f.write(v['value'])
            f.close()

            with open(self.tmpdir + "/" + self.project + ".game" + self.targetid + ".status", "w") as f:
                f.write("success")
            f.close()
            status = 1
        else:

            with open(self.tmpdir + "/" + self.project + ".game" + self.targetid + ".info", "w") as f:
                f.write(v['value'])
            f.close()

            with open(self.tmpdir + "/" + self.project + ".game" + self.targetid + ".status", "w") as f:
                f.write("faild")
            f.close()

        if self.retry:
            self.setServerStatus(self.targetid, self.status, v['value'])
            self.setTaskStatus(self.TaskId, 0, "retry merge-script")
            return

        try:
            url = merge.GAME_PROJ_INFO[self.project]['SingleMergeGameInfoUrl']
            secret = merge.GAME_PROJ_INFO[self.project]['Secret']

            time_stamp = str(time.time()).split('.')[0]

            dic_param = {'tm': time_stamp, 'id': self.id}
            sign = accesses.sign(dic_param, secret)
            dic_param['sign'] = sign

            url += str(urllib.urlencode(dic_param))
            game_data = accesses.get(url)

            if game_data['code'] != 1:
                print "Error MergeThread.run get merge info of targetid:", self.targetid, "err:", game_data
                return

            data = game_data['info'][0]
            time_local = time.localtime(data['merge_time'])
            dt = time.strftime("%Y-%m-%d", time_local)
            tm = time.strftime("%H:%M:00", time_local)

        except:
            dt = ""
            tm = ""
            v ={"value":"get merge-data from webapi"}

        extra_data = {
            'message': v['value'],
            "mdbhost": self.mdbhost,
            "sdbhost": self.sdbhost,
            'opendate': dt,
            'opentime': tm,
            'gameid': self.targetid,
        }

        self.setServer(self.targetid, dt, tm, self.__get_mainhost(), self.project, extra_data, status)
        self.setTaskStatus(self.TaskId, 0, "run merge-script")
