#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys,os,commands
basedir=os.path.abspath(__file__)
basedir=os.path.dirname(basedir)
basedir=os.path.dirname(basedir)
basedir=os.path.dirname(basedir)
basedir=os.path.dirname(basedir)
basedir=os.path.dirname(basedir)
sys.path.append(basedir)
from backend.lib.ssh import *


#拷贝目录
def scp_dir(host, fromdir, todir):
    status, value = cmd(host, "mkdir -p %s" %(todir), 'pirate')
    output = value.strip("\n")
    if output == "1":
        return False
    for f in os.listdir(fromdir):
        scp(host, os.path.join(fromdir,f), os.path.join(todir,f))


#scp_dir('192.168.1.140','/tmp/b','/tmp/b')
