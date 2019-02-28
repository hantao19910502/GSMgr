# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.exceptions import PermissionDenied
import time, json
from .models import *
from django.db import transaction


#  Create your views here.



class GameProjectCreate(CreateView):
    model = GameProject
    fields = ('name', 'codename', 'manager')


class GameProjectList(ListView):
    model = GameProject


class GameProjectUpdate(UpdateView):
    model = GameProject
    fields = ('name', 'codename', 'manager')


class GameProjectDetail(DetailView):
    model = GameProject


class openServerView(TemplateView):
    template_name = 'openserver/openserver.html'

    def post(self, request):
        gameproj = request.POST.get("gameproj", "")
        newservers = request.POST.get("newservers", "")

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

        osr = openServerRecord(request.user.username, gameproj, newservers)
        if not osr.recordinfo():
            return HttpResponse("配置出现问题,请检查!")
        return HttpResponse("success")


class OpenServerTaskList(ListView):
    model = OpenServerTask


class OpenServerTaskDetail(DetailView):
    model = OpenServerTask

    def get_context_data(self, **kwargs):

        context = super(OpenServerTaskDetail, self).get_context_data(**kwargs)
        taskid = self.kwargs["pk"]
        data = []
        try:
            for i in OpenServerTask.objects.get(id=taskid).serveridintask_set.all():

                status = "N/A"
                info = "N/A"

                try:
                    sf = ServerInfomation.objects.get(serverid=i.serverid.split('-')[0])
                    status = sf.get_status_display
                    info = eval(sf.extra_data)['failoutput']
                except Exception,e:
                    print "OpenServerTaskDetail Warning",e


                tmpdt = [i.serverid.split('-')[0], status, info]
                
                try:
                    svinfo = ServerInfomation.objects.get(serverid=i.serverid.split('-')[0])

                    extra_data = svinfo.extra_data

                    if svinfo.status == 1:
                        tmpdt[1] = 'success'
                        tmpdt[2] = 'ok'
                    else:
                        tmpdt[1] = 'faild'
                        tmpdt[2] = json.loads(svinfo.extra_data)['failoutput']
                except Exception,e:
                    print "Error OpenServerTaskDetail ",e

                data.append(tmpdt)

            context['serverinfo'] = data
        except Exception, e:
            print e

        return context


class ServerInfomationList(ListView):
    model = ServerInfomation

    def get_context_data(self, **kwargs):
        context = super(ServerInfomationList, self).get_context_data(**kwargs)
        data = []
        context['hostprojs'] = [( i.name, i.codename) for i in GameProject.objects.all()]

        return context


class ServerInfomationDetail(DetailView):
    model = ServerInfomation


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView).get_context_data(**kwargs)
        return context


class openServerRecord:
    def __init__(self, operator, gameproj, newservers):

        self.operator = operator
        self.gameproj = gameproj
        self.newservers = newservers
        self.operatetime = time.strftime('%Y-%m-%d %X', time.localtime())

    def recordinfo(self):
        try:

            gpj = GameProject.objects.get(codename=self.gameproj)

            with transaction.atomic():

                osl = OpenServerTask.objects.create(
                        description=str(self.gameproj) + " " + " " + str(self.operatetime),
                        operator=User.objects.get(username=self.operator),
                        gameproject=gpj,
                        operatetime=self.operatetime,
                        status=1,
                )
                osl.save()

                if self.newservers.endswith(","):
                    self.newservers = self.newservers[:-1]

                for i in self.newservers.split(","):
                    ServerIdInTask.objects.create(
                            serverid=i,
                            task=osl,
                    )
        except Exception, e:
            print "Error openServerRecord.recordinfo ", e
            return False
        return True
