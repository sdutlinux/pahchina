#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf.urls import patterns, include, url


from . import views


urlpatterns = patterns('',

    url(r'^login/$', views.pah_login, name='login'),
    url(r'^register/$', views.pah_register, name='register'),
    url(r'^logout$', views.pah_logout, name='logout'),

    url(r'^password/reset/$', views.PasswordReset.as_view(), name='password-reset'),

    url(r'^$', views.admin_index, name='admin-index'),

    url(r'^user/list$', views.ListUser.as_view(), name='list-user'),
    url(r'^user/create$', views.CreateUser.as_view(), name='create-user'),
    url(r'^user/(?P<pk>\d+)$', views.DetailUser.as_view(), name='detail-user'),

    url(r'^user/update/(?P<pk>\d+)$', views.UpdateUser.as_view(), name='update-user'),
    url(r'^user/update/(?P<pk>\d+)/password$', views.ListUser.as_view(), name='update-user-password'),

    url(r'^user/delete/(?P<pk>\d+)$', views.DeleteUser.as_view(), name='delete-user'),
)
