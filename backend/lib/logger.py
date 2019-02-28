#!/usr/bin/python
# -*- coding=UTF-8 -*-
import sys,os
import logging
import logging.handlers  
basedir=os.path.abspath(__file__) 
basedir=os.path.dirname(basedir) 
from backend.conf import open
#default
LOG_FILE  = basedir + "/../log/logger.log"

LEVEL= "logging.INFO"

try:
    LOG_FILE = config.LOG_FILE
except:
    pass

try:
    LEVEL= "logging." + config.LOG_LEVEL
except:
    pass

def Logger(level,func,message):

    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5) # 实例化handler   
    fmt = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    formatter = logging.Formatter(fmt)   
    handler.setFormatter(formatter)        
    logger = logging.getLogger(func)    
    logger.addHandler(handler)           
    logger.setLevel(eval(LEVEL))

    output_level_func = "logger." + str(level)
    eval(output_level_func)(message)

if __name__ == "__main__":
    Logger("warn","Logger","this is a logger test")
