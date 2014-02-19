#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^admin/list$', views.ListActivity.as_view(), name='admin-list-activity'),
                       url(r'^admin/(?P<pk>\d+)$', views.DetailActivity.as_view(), name='admin-detail-activity'),
                       url(r'^show/(?P<pk>\d+)$', views.ShowActivity.as_view(), name='show-activity'),
                       url(r'^admin/create$', views.CreateActivity.as_view(), name='admin-create-activity'),
                       url(r'^admin/update/(?P<pk>\d+)$', views.UpdateActivity.as_view(), name='admin-update-activity'),
                       url(r'^admin/delete/(?P<pk>\d+)$', views.DeleteActivity.as_view(), name='admin-delete-activity'),
                       )