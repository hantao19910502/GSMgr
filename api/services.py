#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json
import urllib2


def GetRoleNextLayer(request):
    data=[]
    r = request.GET.get('term')
    url = "http://rolling.stage.babeltime.com/api/role/nextlayer?method=get&term="+str(r)
    req = urllib2.urlopen(url)

    res = req.read()
    return HttpResponse(res, content_type='application/json; charset=utf-8')


def GetHostIpByRole(request):
    data=[]
    r = request.GET.get('term')
    url = "http://rolling.babeltime.com/api/role/ip/filter/"+str(r)
    req = urllib2.urlopen(url)

    res = req.read()
    print 'aaaa',url,res
    return HttpResponse(res, content_type='application/json; charset=utf-8')

