from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^list$', login_required(views.UserListView.as_view()) ,name='user_list'),
    url(r'^profile/edit/(?P<pk>[\w-]+)$',login_required(views.UserProfileUpdate.as_view()),name='user_update'),
    url(r'^profile/detail/(?P<pk>[\w-]+)$',login_required(views.UserDetailView.as_view()),name='user_detail'),
    url(r'^profile/edit$',login_required(views.UserProfileUpdate.as_view()), name="user_edit"),
    url(r'^add$', login_required(views.UserCreateView.as_view())),
]
