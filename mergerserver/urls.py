from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [


    # url(r'^$', cache_page(60 * 60)(login_required(index_view)), name='index'),

    url(r'^opt$', login_required(views.MergerServerView.as_view()), name='opt'),
    url(r'^mergesvtask/list$', (login_required(views.MergerServerTaskList.as_view())), name='mergeservertask_list'),
    url(r'^mergesvtask/detail/(?P<pk>[\w-]+)$', login_required(views.MergerServerTaskDetail.as_view()), name='mergeservertask_detail'),


    # url(r'^hostgroupconfig/add$', login_required(views.HostGroupConfigCreate.as_view()), name='hostgroupconf_create'),
    # url(r'^hostgroupconfig/list$', (login_required(views.HostGroupConfigList.as_view())), name='hostgroupconf_list'),
    # url(r'^hostgroupconfig/edit/(?P<pk>[\w-]+)$', login_required(views.HostGroupConfigUpdate.as_view()), name='hostgroupconf_update'),
    # url(r'^hostgroupconfig/detail/(?P<pk>[\w-]+)$', login_required(views.HostGroupConfigDetail.as_view()), name='hostgroupconf_detail'),
    # url(r'^hostgroupconfig/del/(?P<pk>[\w-]+)$', login_required(views.HostGroupConfigDelete.as_view()), name='hostgroupconf_delete'),

    # url(r'^hostproj/add$', login_required(views.GameProjectCreate.as_view()), name='gameproj_create'),
    # url(r'^hostproj/list$', (login_required(views.GameProjectList.as_view())), name='gameproj_list'),
    # url(r'^hostproj/edit/(?P<pk>[\w-]+)$', login_required(views.GameProjectUpdate.as_view()), name='gameproj_update'),
    # url(r'^hostproj/detail/(?P<pk>[\w-]+)$', login_required(views.GameProjectDetail.as_view()), name='gameproj_detail'),
    #

    #
    # url(r'^serverinfo/list$', (login_required(views.ServerInfomationList.as_view())), name='serverinfo_list'),
    # url(r'^serverinfo/detail/(?P<pk>[\w-]+)$', login_required(views.ServerInfomationDetail.as_view()), name='serverinfo_detail'),



]
