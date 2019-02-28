#!/usr/bin/env python
# -*- coding=UTF-8 -*-


# mysql
MYSQL_ROOT_USER = "root"
MYSQL_ROOT_PASS = "2WTWzvor8qASHZfjII2FNdJKOSwDQ5Rm"
MYSQL_USER = "admin"
MYSQL_PASS = "I7Rt7aZooumVjOfqInTBwbjv03B4Mvao"
DB_MAX_COUNT = 50


# path
HOMEPATH = "/home/pirate"
DATAPROXYPATH = HOMEPATH + "/dataproxy/data"
MAIN_RPCFWPATH= HOMEPATH + "/rpcfw/conf/gsc"
LOGIC_RPCFWPATH= HOMEPATH + "/rpcfw/conf/gsc" 
INITPATH = HOMEPATH + "/rpcfw/script"
MYSQLPATH = HOMEPATH + "/programs/mysql/bin"
MAIN_LCSERVERPATH = HOMEPATH + "/lcserver/conf"

# local path
LOCALHOMEPATH = "/home/pirate/django/GSMgr/backend/var/sanguo"
LOCAL_LCSERVERPATH = LOCALHOMEPATH + "/lcserver"
LOCAL_RPCFWPATH = LOCALHOMEPATH + "/rpcfw"
TEMPLATE_PATH = LOCALHOMEPATH + "/templates"

# rolling set
IP_LIST_API = "http://rolling.babeltime.com/api/role/ip/filter/"

# web url

OPEN_GAME_INFO = "http://192.168.1.38/stat/getserverinfo/getInfoByOneServer"
OPEN_GAME_INFO_SECRET = "platform_ZuiGame_giftBag"

# Globel config
BASE_CONFIG  = {
    "10000":{
	"LogicZKPath":"/card/logic/appstore",
	"WanBasePort":"1000",
	"LanBasePort":"2000",
	},

    "70000":{
        "LogicZKPath":"/card/logic/appstore",
        "WanBasePort":"1000",
        "LanBasePort":"2000", 
        },

    "30000":{
        "LogicZKPath":"/card/logic/appstore",
        "WanBasePort":"1000",
        "LanBasePort":"2000",
        },

   "10400":{
        "LogicZKPath":"/card/logic/appstore",
        "WanBasePort":"1000",
        "LanBasePort":"2000",
        },
    "LcserverMax":50,
    "DatabaseMax":50,
    "BossOffset":[0,900,1800,2700],
    "MAIN":"main.lcserver",
    "LOGIC":"logic.phpproxy",
    "LCConf":"/home/pirate/lcserver/conf",
    "LCTest":"/home/pirate/lcserver",
    "RPCConf":"/home/pirate/rpcfw/conf/gsc",
    "DataproxyPath":"/home/pirate/dataproxy/data",
    "InitPath":"/home/pirate/rpcfw/script",
    "WriteArgs":"-d pirate%s -W %s -L %s -i %s",
    "TemplatePath":"/home/pirate/django/GSMgr/backend/var/templates/sanguo/sample",
}

