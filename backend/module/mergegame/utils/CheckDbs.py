#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys, os
from backend.lib import mysql

class CheckDbs:
    
    def __init__(self,host,port,user,passwd):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
      
    def count_dbs(self,prefix):
        
        sql = "show databases like '" + prefix +"%';" 
        v = mysql.query(self.host, self.port, self.user, self.passwd, sql)

        return len(v)

    def get_mdb(self):
        sql = "show slave status;"
        v = mysql.query(self.host, self.port, self.user, self.passwd,sql)

        return v[0]['Master_Host']



