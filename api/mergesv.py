#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, time, urllib, sys
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from mergerserver.models import *
from openserver.models import *
from backend.conf import merge
from backend.lib import accesses
from backend.scripts import  MergeRun

reload(sys)
sys.setdefaultencoding('utf-8')

class RunScript(object):
    def __init__(self, taskid, retry):
        self.taskid = taskid
        self.retry = retry

    def gogogo(self):
        try:
	    print "xxx=========================================="
            ost = MergerServerTask.objects.get(id=self.taskid)
            serverids = [i.targetid for i in ost.mergergroupintask_set.all()]

            MergeRun.RunAdapter(ost.gameproject.codename, ost.id, ost.gameproject.codename, serverids, self.retry)

        except Exception, e:
            print "Error api.mergesv.RunScript ",e

def RunMergeGameApi(request, taskid):
    success_url = "/mergerserver/mergesvtask/detail/"
    if taskid == "":
        return HttpResponse("fields is empty!")

    retry = False
    try:
        retry = bool(request.POST.get("retry", ""))
    except:
        retry = False

    if not request.user.is_superuser:
        return HttpResponseForbidden("对不起,你没有权限做此操作！")

    t = RunScript(taskid,retry)
    t.gogogo()

    return HttpResponseRedirect(success_url + taskid)



def GetMergeGameInfo(request):
    proj = request.POST.get("gameproj", "")
    begindt = request.POST.get("begindate", "")
    enddt = request.POST.get("enddate", "")

    data = []

    if proj == '' or begindt == '从:' or enddt == '到:':
        return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')
    try:
        merge_url = merge.GAME_PROJ_INFO[proj]['MergeGameInfoUrl']
        secret = merge.GAME_PROJ_INFO[proj]['Secret']
        time_stamp = str(time.time()).split('.')[0]

        projname = GameProject.objects.get(codename=proj).name
        param_dict = {'tm':time_stamp,'begintime': begindt, 'endtime': enddt}

        sign = accesses.sign(param_dict, secret)
        param_dict['sign'] = sign

        merge_url += str(urllib.urlencode(param_dict))
        game_info = accesses.get(merge_url)

        if game_info['code'] != 1:
            return HttpResponse(json.dumps([]), content_type='application/json; charset=utf-8')


        for h in game_info['info']:
            targetid=str(h['groupbase'])

            time_local = time.localtime(h['merge_time'])
            dt = time.strftime("%Y-%m-%d", time_local)
            tm = time.strftime("%H:%M:00", time_local)

            for i in h['str_merge_server'].split(','):
                g = int(i)-int(h['groupbase'])
                targetid+="_"+str(g)

            tmpgm = (projname, h['groupbase'],h['strSid'], dt, tm, targetid,h['id'])

            data.append(tmpgm)



    except Exception,e:
        print "Error GetMergeGameInfo ",e
        return HttpResponse(json.dumps([]), content_type='application/json; charset=utf-8')

    return HttpResponse(json.dumps(data), content_type='application/json; charset=utf-8')


def SetServerTaskStatusApi(request):
    taskid = request.POST.get("taskid", "")
    execoutput = request.POST.get("execoutput", "")
    status = request.POST.get("status", "")

    try:
        ost = MergerServerTask.objects.get(id=taskid)
        if status != 5:
            for i in ost.mergergroupintask_set.all():
                signal = 4
                try:
                    s = ServerInfomation.objects.get(serverid=str(i.targetid.split('.')[1]))
                    if s.status == 2:
                        signal = 3
                except Exception, e:
                    print 'debug',e
                    signal = 2
                    break

            status = signal

        ost.status = status
        ost.execoutput = execoutput
        ost.save()

    except Exception, e:
        print e
        return HttpResponse(json.dumps("faild"), content_type='application/json; charset=utf-8')

    return HttpResponse(json.dumps("success"), content_type='application/json; charset=utf-8')
