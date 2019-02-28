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


#远程执行命令获取返回值
def ssh_return(hostip, comm,  num):
    status, value = cmd(hostip, comm)
    output = value.strip("\n")
    if output == num:
        return True
    else:
        return False
