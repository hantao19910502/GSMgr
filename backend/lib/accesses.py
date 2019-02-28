#!/usr/bin/env python
# -*- coding=UTF-8 -*-
import os, sys
import urllib2, urllib
from hashlib import md5
import time
import collections
import json

class GenerateGignature(object):
    def __init__(self, **kwargs):
        self.dic = collections.OrderedDict()

    def __get_md5sum(self, tosign):
        return md5(tosign).hexdigest()

    def __sorted_parameters_key(self, dic):
        return sorted(dic.keys())

    def __get_sign_string(self, dic_key, dic):
        str_to_sign = ""

        sign_str=""
        for k in dic_key:
            #self.dic[k] = dic[k]
            sign_str+=str(k)+"="+str(dic[k])

        return sign_str
        #return urllib.urlencode(self.dic)

    def get_sign(self, dic, secret):
        keys = self.__sorted_parameters_key(dic)
        sign_str = self.__get_sign_string(keys, dic)
        sign_str = secret + sign_str

        return self.__get_md5sum(sign_str)


class AccessUrl(object):
    def __init__(self):
        pass

    def get_url(self, url):

        req = urllib2.Request(url)
        result = urllib2.urlopen(req)
        return json.loads(result.read())

def sign(param_dic,secret):
    return GenerateGignature().get_sign(param_dic,secret)

def get(url):
    return AccessUrl().get_url(url)


print get("http://192.168.1.38/stat/getserverinfo/mergeServerList?tm=1517394600&id=4&sign=7249a8a6fc2b34a9d0746078ba233666")
