#!/usr/bin/env python
# -*- coding=UTF-8 -*-


ROLE_BY_GROUPBASE_API = "http://rolling.stage.babeltime.com/api/role/getrolebygroupbase/?"
IP_LIST_API = "http://rolling.stage.babeltime.com/api/role/ip/filter/"
SERVICE_LIST_API="http://rolling.stage.babeltime.com/api/service/list/"
TASK_STATUS_API = "http://192.168.1.144:8000/api/mergesv/settaskstatus"
SERVER_SET_API = "http://192.168.1.144:8000/api/addserverinfo"
SERVER_STATUS_SET_API = "http://192.168.1.144:8000/api/setserverstatus"

GAME_PROJ_INFO = {

    "sanguo": {
        "name": "三国",
        "MergeGameInfoUrl": "http://192.168.1.38/stat/getserverinfo/mergeServerList?",
        "SingleMergeGameInfoUrl": "http://192.168.1.38/stat/getserverinfo/mergeServerList?",
        "Secret": "platform_ZuiGame_giftBag",
    },

    "sg2": {
        "name": "三国2",
        "MergeGameInfoUrl": "http://192.168.1.113:17603/gameapi/platform/getNewServerInfo?",
        "Secret": "#babelPfKey@",
    },

    "hhw": {
        "name": "航海王",
        "MergeGameInfoUrl": "http://192.168.1.113:17605/gameapi/platform/getNewServerInfo?",
        "Secret": "#babelPfKey@",
    },

    "sgslg": {
        "name": "裂土封王 ",
        "PlatformUrl": "",
        "GameInfoUrl": "",
        "Secret": "platform_ZuiGame_giftBag",
    },

}
# install app
INSTALL_APPS = {
    "sanguo": "MergeGameSanguo",
    "sg2": "MergeGameSg2",
    "hhw": "MergeGameHhw",
}
