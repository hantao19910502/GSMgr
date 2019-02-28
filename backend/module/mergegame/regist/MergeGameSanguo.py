#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys, os, paramiko
from backend.module.mergegame.frame.CPPframework import MutilMergeGame
from backend.module.mergegame.base.BaseMergeGame import MergeGame
from backend.module.mergegame.conf import sanguo_conf as cf

 
class MergeGameSanguo(MutilMergeGame,MergeGame):
    def __init__(self, *args):
        super(MergeGameSanguo,self).__init__()

        # local params
        self.TaskId = args[0]
        self.Project = args[1]
        self.TargetId = args[2]
        self.Retry = args[3]

        #rewrite
        self.mergehost = cf.MergeHost
        self.mergescript = cf.MergeScript
        self.procnum = cf.MergeProcNum
        self.user = cf.User
        self.passwd = cf.Passwd
        self.sshmode = cf.SSHMode
        self.sshpkey = cf.SSHPkey

        self.sysuser = cf.SysUser
        self.syspasswd = cf.SysPasswd
             
        self.BASE_CONFIG = cf.BASE_CONFIG

    def merge(self):
        self.cpp_merge()

