#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys, os, time

#sys.path.append('/home/pirate/django/GSMgr')
from backend.conf import open
from backend.module.creategame.Adapter import CreateGameAdapter
import threading


class RunThread(threading.Thread):
    def __init__(self, fn, *args):
        super(RunThread, self).__init__()
        self.fn = fn
        self.args = args

    def run(self):
        fn = str(self.fn)
        ag = [i for i in self.args]
        if not open.INSTALL_APPS.has_key(fn):
            print "There is no a function for func_key  \'%s\'  installed!" % fn
            return

        funcname = open.INSTALL_APPS[fn]
        cga = CreateGameAdapter(funcname, *self.args)
	print "=========================test==================================="
        cga.before()
        cga.create()
        cga.after()
        return

def RunAdapter(fn, *args):
    a = RunThread(fn, *args)
    a.start()
    return

#if __name__ == "__main__":
#    RunAdapter("sanguo", "1", "test", [('70001', '72')])
