#!/usr/bin/env python
import os,sys

basedir = os.path.abspath(__file__)
basedir = os.path.dirname(basedir)
basedir = os.path.dirname(basedir)
basedir = os.path.dirname(basedir)
print basedir
sys.path.append(basedir)
from backend.scripts import *


if __name__ == "__main__":
    #CreateRun.RunAdapter("sanguo", "12", "sanguo", ["600002", "700003", "500004", "300005"])
    #MergeRun.RunAdapter("sanguo", "12", "sanguo", ["600002", "700003", "500004", "300005"])

    print 'hello'
