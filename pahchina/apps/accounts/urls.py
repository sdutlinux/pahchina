#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_reset
from django.core.urlresolvers import reverse_lazy, reverse
from ..region import views as region_views

from . import views
import generic


urlpatterns = patterns('',

    url(r'^$', views.admin_index, name='admin-index'),

    url(r'^login/$', views.pah_login, name='login'),
    url(r'^register/$', views.pah_register, name='register'),
    url(r'^logout$', views.pah_logout, name='logout'),

    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    url(r'^update/profile/$', views.UpdateProfile.as_view(), name='update-profile'),

    url(r'^show/(?P<pk>\d+)/$', views.Show.as_view(), name='show'),

    # region
    url(r'region/(?P<cate>\w+)/$', region_views.UserSetRegion.as_view(), name='user-region'),


    # generic
    url(r'^update/(?P<model>\w+)/(?P<pk>\d+)/$', generic.Update.as_view(), name='admin-update'),
    url(r'^delete/(?P<model>\w+)/(?P<pk>\d+)/$', generic.Delete.as_view(), name='admin-delete'),
    url(r'^detail/(?P<model>\w+)/(?P<pk>\d+)/$', generic.Detail.as_view(), name='admin-detail'),
    url(r'^create/(?P<model>\w+)/$', generic.Create.as_view(), name='admin-create'),
    url(r'^list/(?P<model>\w+)/$', generic.List.as_view(), name='admin-list'),


    url(r'^(?P<model>\w+)/$', views.UserInfoView.as_view(), name='user-info'),
    url(r'^update/(?P<model>\w+)/$', views.UpdateUserInfo.as_view(), name='update-info'),

    url(r'^password/update/$', views.UpdatePassword.as_view(), name='update-password'),
)

urlpatterns += patterns('',

    url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/accounts/user/password/reset/done/',},
        name="password-reset"),
    url(r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done',
        name='password-reset-done'),
    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/accounts/user/password/done/'}),
    url(r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete', name='password-reset-complete'),
)
