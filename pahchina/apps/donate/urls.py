#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'


from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^admin/list/$', views.ListDonate.as_view(), name='admin-list-donate'),
                       url(r'^admin/(?P<pk>\d+)/$', views.DetailDonate.as_view(), name='admin-detail-donate'),
                       url(r'^admin/create/$', views.CreateDonate.as_view(), name='admin-create-donate'),
                       url(r'^admin/update/(?P<pk>\d+)/$', views.UpdateDonate.as_view(), name='admin-update-donate'),
                       url(r'^admin/delete/(?P<pk>\d+)/$', views.DeleteDonate.as_view(), name='admin-delete-donate'),
                       url(r'^test/$', views.CreateDonateUser.as_view(), name='donate'),

                       )