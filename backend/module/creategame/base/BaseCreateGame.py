#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import sys,os,urllib2,urllib,json,MySQLdb,commands

class CreateGame(object):
    def __init__(self):
        self.TASK_STATUS_API = None
        self.SERVER_RECORD_API = None
        self.IP_LIST_API = None
        self.SERVICE_LIST_API = None

    def before(self):
        pass

    def create(self):
        pass

    def after(self):
        pass


    def _post_task_status(self,taskid,status,execoutput):

        try:
            url = self.TASK_STATUS_API
	    print 'url:',url
            values = {'taskid':taskid,'status':status,'execoutput':execoutput}
	    print 'values:',values
            data = urllib.urlencode(values)
	    print 'data:',data
            req = urllib2.Request(url, data)
	    print 'req:',req
            response = urllib2.urlopen(req)
	    print 'response:',response
            if json.loads(response.read()) == 'success':
                return True
            else:
                return False
        except Exception,e:
            print e
            return False

    def _record_server_info(self,serverid,opendate,opentime,serverhost,gameproject,extra_data,status):
        try:
            url = self.SERVER_RECORD_API
            values = {'serverid':serverid,'opendate':opendate,'opentime':opentime,'serverhost':serverhost,
                      'gameproject':gameproject,'extra_data':extra_data,'status':status}

            data = urllib.urlencode(values)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)

            if json.loads(response.read()) ==  'success':
                return True
            else:
                return False
        except Exception,e:
            print e
            return False

    def get_host_list(self, key):

        try:
            resp = json.loads(urllib2.urlopen(self.IP_LIST_API + key).read())
            return [ip["ip"] for ip in resp]
        except:
            return None

    def get_service_info(self,role):
        data = []
        try:
            url = self.SERVICE_LIST_API+role
            data = urllib2.urlopen(url)
        except Exception,e:
            return []

        return json.loads(data.read())

