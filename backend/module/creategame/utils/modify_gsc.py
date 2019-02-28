#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys,os,shutil



#修改GSC文件
def modify_gsc(opendate, opentime, offset,rpcfwpath):
    f = open(os.path.join(rpcfwpath, 'Game.cfg.php'),'r')
    f_new = open(os.path.join(rpcfwpath, 'Game.cfg.php.bak'),'w')
    for line in f:
        if "old_opendate" in line:
            line = line.replace('old_opendate', opendate)
        if "old_opentime" in line:
            line = line.replace('old_opentime', opentime)
        if "old_offset" in line:
            line = line.replace('old_offset', str(offset))
        f_new.write(line)
    f.close()
    f_new.close()
    shutil.move(os.path.join(rpcfwpath, 'Game.cfg.php.bak'),os.path.join(rpcfwpath, 'Game.cfg.php'))
    os.chmod(os.path.join(rpcfwpath, 'Game.cfg.php'), 0755)

