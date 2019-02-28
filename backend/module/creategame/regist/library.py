#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import MySQLdb, commands
import os, sys
import urllib2, urllib
from hashlib import md5
import time
import collections
import json


def create_game_tools(obj, *args):
    templates = {"template": TemplateConfig, "copyfile": CopyFileToHost, "remoteshell": ExeRomoteHostCmd,
                 "mysqlconn": ExeRemoteMysqlCmd, "test": Test}
    temp = None
    try:
        temp = templates[obj](*args)
    except Exception, e:
        print e
        return False

    return temp.running()


class BaseTools(object):
    def __init__(self):
        pass

    def running(self):
        pass


class Test(BaseTools):
    def __init__(self, a):
        self.a = a

    def test(self, a):
        print False, a

    def running(self):
        return self.test(self.a)


class TemplateConfig(BaseTools):
    def __init__(self):
        pass

    def gen_args(self):
        pass

    def running(self):
        self.gen_args()


class CopyFileToHost(BaseTools):
    def __init__(self):
        pass

    def copy(self):
        pass

    def running(self):
        self.copy()


class ExeRomoteHostCmd(BaseTools):
    def __init__(self):
        pass

    def exe_remote_cmd(self):
        pass

    def running(self):
        self.exe_remote_cmd()


class ExeLocalHostCmd(BaseTools):
    def __init__(self, cmd):
        self.cmd = cmd

    def local_shell_exe_cmd(self, cmd):
        try:
            (status, output) = commands.getstatusoutput(cmd)
            if status != 0:
                return False, output
        except Exception, e:
            return False, e

        return True, output

    def running(self):
        return self.local_shell_exe_cmd(self.cmd)


class ExeRemoteMysqlCmd(BaseTools):
    def __init__(self, host, port, user, passwd, sql):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.sql = sql

    def conn_mysql_exe_cmd(self, host, port, user, passwd, sql):
        result = None
        try:
            conn = MySQLdb.connect(host=host, user=user, passwd=passwd, port=port)
            cur = conn.cursor()
            count = cur.execute(sql)
            result = cur.fetchall()
            cur.close()
            conn.close()
        except Exception, e:
            return False, e

        return True, result

    def running(self):
        return self.conn_mysql_exe_cmd(self.host, self.port, self.user, self.passwd, self.sql)


class GenerateGignature(object):
    def __init__(self, **kwargs):
        self.dic = collections.OrderedDict()

    def __get_md5sum(self, tosign):
        return md5(tosign).hexdigest()

    def __sorted_parameters_key(self, dic):
        return sorted(dic.keys())

    def __get_sign_string(self, dic_key, dic):
        str_to_sign = ""

        sign_str=""
        for k in dic_key:
            #self.dic[k] = dic[k]
            sign_str+=str(k)+"="+str(dic[k])

        return sign_str
        #return urllib.urlencode(self.dic)

    def get_sign(self, dic, secret):
        keys = self.__sorted_parameters_key(dic)
        sign_str = self.__get_sign_string(keys, dic)
        sign_str = secret + sign_str

        return self.__get_md5sum(sign_str)


class AccessUrl(object):
    def __init__(self):
        pass

    def get_url(self, url):

        try:
            req = urllib2.Request(url)
            result = urllib2.urlopen(req)
            return json.loads(result.read())
        except Exception, e:
            return {"code": 2, "rmg": e}
