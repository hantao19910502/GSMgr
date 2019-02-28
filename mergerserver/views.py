# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import time,json
from openserver.models import GameProject
from mergerserver.models import *
from openserver.models import ServerInfomation
from django.db import transaction

# Create your views here.

class MergerServerTaskList(ListView):
    model = MergerServerTask

class MergerServerTaskDetail(DetailView):
    print "---------------------------------"
    model = MergerServerTask
    print "---------------------------------"

    def get_context_data(self, **kwargs):

        context = super(MergerServerTaskDetail, self).get_context_data(**kwargs)
        taskid = self.kwargs["pk"]
        data = []
        try:
            for i in MergerServerTask.objects.get(id=taskid).mergergroupintask_set.all():

                status = "N/A"
                info = "N/A"

                try:
                    sf = ServerInfomation.objects.get(serverid=i.targetid.split('.')[1])
                    status = sf.get_status_display
                    info = eval(sf.extra_data)['message']

                except Exception, e:
                    pass
                tmpdt = [i.targetid.split('.')[1], status, info]

                try:
                    svinfo = ServerInfomation.objects.get(serverid=i.targetid.split('.')[1])
                    if svinfo.status == 1:
                        tmpdt[1] = svinfo.status
                    else:
                        failoutput = json.loads(svinfo.extra_data)['message']
                        tmpdt[2] = failoutput
                except Exception,e:
                    print e

                data.append(tmpdt)

            context['serverinfo'] = data
        except Exception, e:
            print 'MergerServerTaskDetail ',e

        return context


class MergerServerView(TemplateView):
    template_name = 'mergerserver/mergerserver.html'

    def post(self, request):
        gameproj = request.POST.get("gameproj", "")
        mergerservers = request.POST.get("mergerservers", "")

        mergesvs = mergerservers.split(',')

        signal = False
        try:
            hp = GameProject.objects.get(codename=gameproj)

            for i in hp.owners.all():
                if i.username == request.user.username:
                    signal = True

            if self.request.user.is_superuser:
                signal = True

            if hp.manager.username == request.user.username:
                signal = True

        except:
            return HttpResponse("提交数据有误！")

        if not signal:
            return HttpResponse("你没有权限！")

        osr = mergerServerRecord(request.user.username, gameproj, mergesvs)
        if not osr.recordinfo():
            return HttpResponse("配置出现问题,请检查!")
        return HttpResponse("success")

class mergerServerRecord(object):
    def __init__(self,username, gameproject, mergerservers):
        self.username = username
        self.gameproject = gameproject
        self.mergerservers = mergerservers

        self.operatetime = time.strftime('%Y-%m-%d %X', time.localtime())

    def recordinfo(self):

        try:

            if len(self.mergerservers)==0:
                print "mergerServerRecord recordinfo error , ready for merger group is empty"
                return False

            with transaction.atomic():
                mst = MergerServerTask.objects.create(
                    description=str(self.gameproject) + " " + " " + str(self.operatetime),
                    operator=User.objects.get(username=self.username),
                    gameproject=GameProject.objects.get(codename=self.gameproject),
                    status=1,
                )
                mst.save()

                for k in self.mergerservers:
                    mgt = MergerGroupInTask.objects.create(
                        task=mst,
                        targetid=k
                    )
                    mgt.save()


        except Exception,e:
            print "mergerServerRecord recordinfo error" ,e
            return False

        return True
