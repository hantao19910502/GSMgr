#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys,os,commands


#本地执行命令
def local_cmd(b):
    (status, output) = commands.getstatusoutput('%s'%(b))
    if status != 0:
        return False
    else:
        return True


