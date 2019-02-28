#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys, os, time

from backend.conf import merge
from backend.module.mergegame.Adapter import MergeGameAdapter
import threading


class RunThread:
    def __init__(self, fn, *args):
        self.fn = fn
        self.args = args

    def runmerge(self):
        fn = str(self.fn)
        ag = [i for i in self.args]
        if not merge.INSTALL_APPS.has_key(fn):
            print "There is no a function for func_key  \'%s\'  installed!" % fn
            return

        funcname = merge.INSTALL_APPS[fn]
        cga = MergeGameAdapter(funcname, *self.args)
        cga.merge()

def RunAdapter(fn, *args):
    a = RunThread(fn, *args)
    a.runmerge()

if __name__ == "__main__":
    RunAdapter("sanguo", "12", "sanguo", ["600002", "700003", "500004", "300005"])
