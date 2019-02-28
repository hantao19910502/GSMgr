#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, time
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from openserver.models import *
from backend.scripts.CreateRun import RunAdapter
from backend.conf import open
from backend.lib import accesses


class RunScript(object):
    def __init__(self, taskid):
        self.taskid = taskid

    def gogogo(self):
        try:
	    gameproject_id = OpenServerTask.objects.filter(id=self.taskid).values('gameproject_id')[0]['gameproject_id']
	    gameproject = GameProject.objects.filter(id=gameproject_id).values('codename')[0]['codename']
	    ost = ServerIdInTask.objects.filter(task_id=self.taskid)
	    serverids=[] 
	    for i  in ost:
		i = str(i)
            	s = i.split('-')
            	serverids.append((str(s[0]), str(s[1])))


            RunAdapter(gameproject, self.taskid, gameproject, serverids)
        except Exception, e:
            print e

def RunCreateGameApi(request, taskid):
    success_url = "/openserver/opensvtask/detail/"
    if taskid == "":
        return HttpResponse("fields is empty!")

    if not request.user.is_superuser:
        return HttpResponseForbidden("对不起,你没有权限做此操作！")

    t = RunScript(taskid)
    t.gogogo()

    return HttpResponseRedirect(success_url + taskid)


def GetGameProject(request):
    data = []
    try:

        for p in GameProject.objects.all():
            data.append((p.name, p.codename))

    except Exception, e:
        print "Error opensv.GetGameProject ",e
    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')


def GetGameInfo(request):
    proj = request.POST.get("gameproj", "")
    begindt = request.POST.get("begindate", "")
    enddt = request.POST.get("enddate", "")

    game_info=""

    data = []

    if proj == '' or begindt == '从:' or enddt == '到:':
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

    plat=''

    try:

        begindt=time.strptime(begindt, "%Y-%m-%d")
        begindt=str(time.mktime(begindt)).split('.')[0]

        enddt=time.strptime(enddt, "%Y-%m-%d")
        enddt=str(time.mktime(enddt)).split('.')[0]

        game_url = open.GAME_PROJ_INFO[proj]['GameInfoUrl']
        plat_url = open.GAME_PROJ_INFO[proj]['PlatformUrl']
        secret = open.GAME_PROJ_INFO[proj]['Secret']
        projname = open.GAME_PROJ_INFO[proj]['name']

        plats = {}
        time_stamp = str(time.time()).split('.')[0]

        dic_plat = {'tm': time_stamp}
        sign = accesses.sign(dic_plat, secret)

        dic_plat['sign'] = sign
        plat_url += str(urllib.urlencode(dic_plat))

        for p in accesses.get(plat_url)['info']:
            plats[p['lid']] = p['lname']

        time_stamp = str(time.time()).split('.')[0]
        dic = {'tm': time_stamp, 'lid': plat, 'beginTime': begindt, 'endTime': enddt}

        sign = accesses.sign(dic, secret)
        dic['sign'] = sign

        game_url += str(urllib.urlencode(dic))
        game_info = accesses.get(game_url)

        if game_info['code'] != 1:
            return HttpResponse(json.dumps([]), content_type='application/json; charset=utf-8')


        for g in game_info['info']:
            time_local = time.localtime(g['openDateTime'])
            dt = time.strftime("%Y-%m-%d", time_local)
            tm = time.strftime("%H:%M:00", time_local)
            tmpsv = (projname, plats[g['lid']], str(g['sid']), str(dt), str(tm), str(g['groupid']), str(g['lid']))
            data.append(tmpsv)

    except Exception, e:
        print "Error GetGameInfo: ", e, game_info
        return HttpResponse(json.dumps([]), content_type='application/json; charset=utf-8')

    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')


def SetServerTaskStatusApi(request):
    taskid = request.POST.get("taskid", "")
    execoutput = request.POST.get("execoutput", "")
    status = request.POST.get("status", "")

    try:
        ost = OpenServerTask.objects.get(id=taskid)
        ost.status = status
        ost.execoutput = execoutput
        ost.save()
    except Exception, e:
        print "Error opensv.SetServerTaskStatusApi ",e
        return HttpResponse(json.dumps("faild"), content_type='application/json; charset=utf-8')

    return HttpResponse(json.dumps("success"), content_type='application/json; charset=utf-8')



def GetServerStatusListApi(request):
    data = []
    gameproj = request.POST.get("hostproj", "")
    if gameproj == "None":
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    try:
        for i in GameProject.objects.get(codename=gameproj).serverinfomation_set.all():
            data.append([i.id, i.serverid, i.status])

    except Exception, e:
        print "Error opensv.GetServerStatusListApi" ,e

    # print 'serverstatus', data,'project',gameproj

    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')


def ServerInfomationCreateApi(request):
    data = 'success'
    
    serverid = request.POST.get('serverid', '')
    opendate = request.POST.get('opendate', '')
    opentime = request.POST.get('opentime', '')
    serverhost = request.POST.get('serverhost', '')
    extra_data = request.POST.get('extra_data', '')
    status = request.POST.get('status', '')
    gameproject = request.POST.get('gameproject', '')
    
    print "debug",gameproject
    print opendate
    try:
        p = GameProject.objects.get(codename=gameproject)
        ServerInfomation.objects.create(
                serverid=serverid,
                opendate=opendate,
                opentime=opentime,
                serverhost=serverhost,
                extra_data=extra_data,
                status=status,
                gameproject=p,
        )

    except Exception, e:
        print "Error opensv.ServerInfomationCreateApi ",e
        data = "faild"

    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')

def ServerInfomationStatusApi(request):

    data = 'success'
    serverid = request.POST.get('serverid', '')
    status = request.POST.get('status', '')
    exeoutput = request.POST.get('output', '')

    try:
        sf = ServerInfomation.objects.get(serverid=serverid)
        sf.status = status
        data = json.loads(sf.extra_data)
        data['message'] = exeoutput
        sf.extra_data = data
        sf.save()
    except Exception,e:
        print 'Error ServerInfomationStatusApi ',e
        data = 'faild'

    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
