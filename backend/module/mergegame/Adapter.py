#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys,os
from backend.module.mergegame.regist import *
from backend.conf import merge
class MergeGameAdapter:

    def __init__(self,fn,*args):
        self.args=args
        self.func=eval(fn)(*args)

    def merge(self):
        self.func.merge()
