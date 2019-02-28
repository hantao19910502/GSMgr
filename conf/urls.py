from django.conf.urls import include, url
from django.contrib import admin
from  userinfo.views import login_view, logout_view, logged_view, index_view
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
urlpatterns = [
    # Examples:
    # url(r'^$', 'keeper.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', (login_required(index_view)), name='index'),
    url(r'^accounts/login/$', login_view, name='login'),
    url(r'^accounts/logout/$', logout_view, name='login_out'),
    url(r'^user/logged$', logged_view),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^userinfo/', include('userinfo.urls', namespace='userinfo')),
    url(r'^openserver/', include('openserver.urls', namespace='openserver')),
    url(r'^mergerserver/', include('mergerserver.urls', namespace='mergerserver')),
    url(r'^api/', include('api.urls', namespace='api')),

]
