#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import urllib
import urllib2
import json


class BaseUtils(object):
    def __init__(self):
        self.SERVER_SET_API = None
        self.TASK_SET_STATUS_API = None

    def setServer(self, serverid, opendate, opentime, serverhost, gameproject, extra_data, status):

        url = self.SERVER_SET_API
        values = {'serverid': serverid, 'opendate': opendate, 'opentime': opentime, 'serverhost': serverhost,
                  'gameproject': gameproject, 'extra_data': extra_data, 'status': status}

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)

        if json.loads(response.read()) != 'success':
            return False

        return True

    def setTaskStatus(self, taskid, status, execoutput):

        url = self.TASK_SET_STATUS_API
        values = {'taskid': taskid, 'status': status, 'execoutput': execoutput}

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)

        if json.loads(response.read()) != 'success':
            return False

        return True

    def setServerStatus(self, serverid, status, execoutput):

        url = self.SERVER_STATUS_SET_API
        values = {'taskid': serverid, 'status': status, 'execoutput': execoutput}

        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)

        if json.loads(response.read()) != 'success':
            return False

        return True
