#!/usr/bin/env python
# -*- coding=UTF-8 -*-
from backend.module.creategame.base.BaseCreateGame import  CreateGame
from backend.module.creategame.regist import *

import sys,os

class CreateGameAdapter(CreateGame):

    def __init__(self,func,*args):
        self.args=args
        self.func=eval(func)(*args)

    def before(self):
        self.func.before()

    def create(self):
        self.func.create()

    def after(self):
        self.func.after()
