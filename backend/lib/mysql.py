#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import MySQLdb, commands
import os, sys
import time
import json

class MysqlConn:
    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def query(self,sql):
        result = None
        conn = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port)
        cur = conn.cursor()
        count = cur.execute(sql)
        result = cur.fetchall()
        columns = cur.description

        res = []
        for s in result:
            tmp={}
            for (index, column) in enumerate(s):
                tmp[columns[index][0]] = column
            res.append(tmp)

        cur.close()
        conn.close()

        return res

def query(host,port,user,passwd,sql):
    m = MysqlConn(host,port,user,passwd)
    return m.query(sql)



