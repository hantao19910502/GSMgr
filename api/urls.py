from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [

    url(r'^role/nextlayer$', 'api.services.GetRoleNextLayer', name="api_rolenextlayer"),
    url(r'^getgameproj$', 'api.opensv.GetGameProject', name="api_getgameproj"),
    url(r'^getgameinfo$', 'api.opensv.GetGameInfo', name="api_getgameinfo"),

    url(r'^getmergegameinfo$', 'api.mergesv.GetMergeGameInfo', name="api_getmergegameinfo"),

    url(r'^addserverinfo$', 'api.opensv.ServerInfomationCreateApi', name="api_addserverinfo"),
    url(r'^setserverstatus$', 'api.opensv.ServerInfomationStatusApi', name="api_setserverstatus"),

    url(r'^opensv/settaskstatus$', 'api.opensv.SetServerTaskStatusApi', name="api_settaskstatus"),
    url(r'^mergesv/settaskstatus$', 'api.mergesv.SetServerTaskStatusApi', name="api_settaskstatus"),

    url(r'^getserverstatuslist$', 'api.opensv.GetServerStatusListApi', name="api_getserverstatuslist"),

    url(r'^creategame/(.+)/$', 'api.opensv.RunCreateGameApi', name="api_creategame"),
    url(r'^mergegame/(.+)/$', 'api.mergesv.RunMergeGameApi', name="api_mergegame"),

]
