#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys,os
basedir=os.path.abspath(__file__)
basedir=os.path.dirname(basedir)
basedir=os.path.dirname(basedir)
sys.path.append(basedir)

from config import config
sys.path.append(basedir+"/package")
from BaseCreateGame import CreateGame
from CPPFramework import CPPFramework

class Test(CreateGame,CPPFramework):

    def __init__(self,*args):
        self.proj=args[0]
        self.plat=args[1]
        self.serverids=args[2]

    def get_info_by_sid(self):

	print 'task:',self.proj,self.plat
	for i in self.serverids:
            print 'need create:',i

    def get_tmp_db(self):
        pass

    def start_serverid(self,serverid):
        print 'start lcserver:', serverid

    def gen_lc_conf(self):
        pass

    def copy_lc_conf(self):
        pass

    #overwrite
    def record(self,serverid,opendate,opentime,serverhost,hostproject,hostgroup,extra_data,status):
        print 'record:',serverid,opendate,opentime,serverhost,hostproject,hostgroup,extra_data,status
        self.get_host_list('sanguo.android.main.lcserver')

    def before(self):
	self.get_info_by_sid()

    def create(self):
        print "test create"

    def after(self):
        print "test after"
        self.start_serverid(30002)
        self.record(1,2,3,4,5,6,7,8)




# 1, 如实例所示,创建一个待适配类Test需要继承 CreateGame类. CreateGame 抽象了三个方法,分别是before create after.根据实际需求重写即可.
# 2, 创建的类需要在config.py INSTALL_APPS 中注册名字.注册名字需与开服系统中定义的项目名一致.以供程序适配.调用方法如:INSTALL_APPS = {"test":"Test",}
# 3, 创建的类都需要在install_modules.py 中进行导入. 如: from test_create import Test
