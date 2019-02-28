#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
   * File Name : views.py

   * Purpose :

   * Creation Date : 15-01-2015

   * Last Modified :

   * Created By : dren
'''
import logging
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.views.generic.list import ListView
from django.views.generic import View
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.contrib.auth.decorators import login_required
import sys
import time
import json
import urllib
import urllib2
from requests import Request, Session
from hashlib import md5
from openserver.models import *
# from ldap3 import Server, Connection, SYNC, AUTH_SIMPLE

from .models import User
from .forms import *
logger = logging.getLogger(__name__)

class BournceBackend:
    appkey = 'bbdcd6a4191827a77fc65972'

    appid = 9
    token = 'BabelTimeToken'
    tokenUrl = 'https://bouncer.babeltime.com/token/check'
    redirect = 'http://' + settings.HOST_PORT + '/user/logged'
    userUrl = 'https://bouncer.babeltime.com/user'
    logout_url = 'https://bouncer.babeltime.com/user/logout'

    def getSign(self, request):

        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        data = [("appid", self.appid), ("ts", int(time.time())),
                ("redirect", 'http://' + request.get_host() + '/user/logged')]
        request.session["next"] = request.GET.get('next', "")
        tmp = ''
        for d in data:
            tmp += d[0] + str(d[1])
        tmp += self.appkey
        sign = md5(tmp).hexdigest()
        data.append(("sign", sign))
        request.session["ts"] = data[1][1]
        return urllib.urlencode(data), sign

    def login(self, request):
        token = request.session.get("token", "")
        logger.info("token ssio:", token)
        if token:
            return self.isLogin(request, token)
        token = request.GET.get("BabelTimeToken", "")
        if token:
            request.session['token'] = token
        args, sign = self.getSign(request)
        goto = self.userUrl + '/login?' + args
        request.session['sign'] = sign
        # print sign, "\t", args, "\t", goto
        return HttpResponseRedirect(goto)

    def isLogin(self, request, token):
        # s = Session()
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        data = [("appid", self.appid),
                ("ip", ip),
                ("token", request.session["token"]),
                ("ts", int(time.time()))
                ]
        tmp = ''
        for d in data:
            tmp += d[0] + str(d[1])
        tmp += self.appkey
        logger.info(tmp, "\t", md5(tmp).hexdigest())
        sign = md5(tmp).hexdigest()
        data.append(("sign", sign))

        resp = json.loads(urllib2.urlopen(self.tokenUrl, urllib.urlencode(data)).read())
        username = resp["info"]["username"]
        logger.info(resp)
        if username:
            request.session["username"] = username
            user = self.get_or_create_user(username, "")
            user.backend = "userinfo.views.BournceBackend"
            request.user = user
            login(request, user)
            return HttpResponseRedirect(request.session.get("next", "/"))
        else:
            return HttpResponse("403")
            # pre = Request('POST', self.tokenUrl, data).prepare()
            # resp = s.send(pre)
            # return resp.text

    def logout(self,request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        data = [("appid", self.appid),
                ("ip", ip),
                ("token", request.session.get("token","")),
                ("ts", int(time.time()))
                ]
        tmp = ''
        for d in data:
            tmp += d[0] + str(d[1])
        tmp += self.appkey
        logger.info(tmp, "\t", md5(tmp).hexdigest())
        sign = md5(tmp).hexdigest()
        data.append(("sign", sign))

        resp = json.loads(urllib2.urlopen(self.logout_url, urllib.urlencode(data)).read())

        return resp

    def authenticate(self, request, token=None):
        try:
            if not request.session.get('token', ""):
                return self.login(request)
            else:
                request.user = self.get_or_create_user(username, 'bouncer')
                return self.get_or_create_user(username, 'bouncer')
        except:
            return None
            # return self.get_or_create_user(username, password)

    def get_or_create_user(self, username, password):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            info = sys.exc_info()
            logger.info(info[0], ":", info[1])
            logger.info(username)
            mail = username + '@babeltime.com'
            user = User(username=username, email=mail)
            user.is_staff = True
            user.is_superuser = False
            user.set_password('ldap a authenticated')
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None  # > 其中域控服务器和用户名，邮箱地址根据实际情况修改。


def logged_view(request):
    token = request.GET.get("BabelTimeToken", "")
    logger.info("token:", token)
    if token:
        request.session['token'] = token
        b = BournceBackend()
        return b.isLogin(request, token)
    else:
        return HttpResponseRedirect(request.session.get("next", "/user/list"))


def login_view(request):
    # if "192.168" not in settings.HOST_PORT and "127.0.0.1" not in settings.HOST_PORT:
    if request.method == "GET":
        request.session["next"] = request.GET.get("next", "")
        b = BournceBackend()
        return b.login(request)

    if request.method == "POST":
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")
        user = authenticate(username=username, password=password)  # 校验处理
        if user is not None:  # 表示校验成功了
            login(request, user)
            if user.is_active:
                # if "frontend" in user.groups.all():
                return HttpResponseRedirect(request.session.get("next", "/user/list"))
                # else:
                #     return HttpResponseRedirect("/frontend/svn/")
            else:
                failed = "Your account has been disabled!"
                return render_to_response("login.html", {"failed": failed})
        else:
            failed = "用户名或密码错误"
            return render_to_response("login.html", {"failed": failed})
    else:
        request.session["next"] = request.GET.get("next", "")
        return render_to_response("login.html")


def logout_view(request):

    c = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
    <html>
    <head>
    <title>Redirecting....</title>
    <body>
    You're logged out.
    </body>
    </html>'''
    #print "del seesion key:", request.session.session_key


    b = BournceBackend()
    x=b.logout(request)
    for sesskey in request.session.keys():
        logger.info("del seesion key:", sesskey)
        del request.session[sesskey]
    request.session.flush()
    logout(request)
    json.dumps(x)
    proto,rest = urllib.splittype(request.META['HTTP_REFERER'])
    res, rest = urllib.splithost(rest)
    return HttpResponseRedirect(rest)


def change_password(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            u = User.objects.get(username__exact=request.user)
            u.set_password(password1)
            u.save()
            return HttpResponse("更改成功")
        else:
            return render_to_response('change_password.html', {"failed": "两次密码不一致", "username": request.user})
    if request.method == "GET":
        # update_session_auth_hash(request, form.user)
        return render_to_response('change_password.html', {"username": request.user})


class UserListView(ListView):
    model = User
    template_name = "userinfo/user_list.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return [self.request.user]

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        return context


class UserProfileUpdate(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = '/user/list'
    template_name_suffix = '_update_form'

    def get_object(self, *args, **kwargs):
        user = User.objects.get(username=self.request.user)
        if user.is_superuser and not self.slug_field:
            obj = super(UserProfileUpdate, self).get_object(*args, **kwargs)
            # if not obj == self.request.user:
            #    raise PermissionDenied
            return obj
        else:
            return user


class UserDetailView(DetailView):
    model = User


class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'userinfo/user_update_form.html'


@login_required()
def index_view(request):

    t = loader.get_template('home.html')

    task_sum=len(OpenServerTask.objects.all())
    new_task_sum=len(OpenServerTask.objects.filter(status=1))
    fail_server_sum=len(ServerInfomation.objects.filter(status=2))

    c = Context({
        'user': request.user,
        'count':{'task_sum':task_sum,
                 'new_task_sum':new_task_sum,
                 'fail_server_sum':fail_server_sum,
                 }
    })

    return HttpResponse(t.render(c))
