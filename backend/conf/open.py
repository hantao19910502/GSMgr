#!/usr/bin/env python
# -*- coding=UTF-8 -*-

# gsmgr api set
TASK_STATUS_API = "http://192.168.2.93:8000/api/opensv/settaskstatus"
SERVER_RECORD_API = "http://192.168.2.93:8000/api/addserverinfo"
HOSTGROUP_INFO = "http://192.168.2.93:8000/api/hostgroupinfo"
IP_LIST_API = "http://rolling.stage.babeltime.com/role/ip/filter/"
SERVICE_LIST_API = "http://rolling.stage.babeltime.com/api/service/list/"
# log path
LOG_LEVEL = "INFO"
LOG_FILE = "openserver.log"
# game project infomation configure from web
MYSQL_USER="admin"
#MYSQL_PASS="I7Rt7aZooumVjOfqInTBwbjv03B4Mvao"
MYSQL_PASS="admin123"
MYSQL_ROOT_USER="root"
MYSQL_ROOT_PASS="2WTWzvor8qASHZfjII2FNdJKOSwDQ5Rm"
GAME_PROJ_INFO = {

    "sanguo": {
        "name": "三国",
        "PlatformUrl": "http://192.168.1.38/stat/getserverinfo/getPlatformsInfo?",
        "GameInfoUrl": "http://192.168.1.38/stat/getserverinfo/getServerInfo?",
        "Secret": "platform_ZuiGame_giftBag",
    },

    "sg2": {
        "name": "三国2",
        "PlatformUrl": "http://192.168.1.113:17603/gameapi/platform/getPlatformsInfo?",
        "GameInfoUrl": "http://192.168.1.113:17603/gameapi/platform/getNewServerInfo?",
        "Secret": "#babelPfKey@",
    },

    "hhw": {
        "name": "航海王",
        "PlatformUrl": "http://192.168.1.113:17605/gameapi/platform/getPlatformsInfo?",
        "GameInfoUrl": "http://192.168.1.113:17605/gameapi/platform/getNewServerInfo?",
        "Secret": "#babelPfKey@",
    },

    "sgslg": {
        "name": "裂土封王 ",
        "PlatformUrl": "",
        "GameInfoUrl": "",
        "Secret": "platform_ZuiGame_giftBag",
    },
    "test": {                                                                   
         "name": "三国",                                                           
         "PlatformUrl": "http://192.168.1.38/stat/getserverinfo/getPlatformsInfo?",
         "GameInfoUrl": "http://192.168.1.38/stat/getserverinfo/getServerInfo?",   
         "Secret": "platform_ZuiGame_giftBag",                                     
    },

    "DatabaseMax":50, 
    "LcserverMax":50,
}

# install app

INSTALL_APPS = {
    "test": "Test",
    "sanguo": "CreateGameSanguo",
}
