#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
                       url(r'^activity/list$', views.ListActivity.as_view(), name='list-activity'),
                       url(r'^activity/(?P<pk>\d+)$', views.DetailActivity.as_view(), name='detail-activity'),
                       url(r'^activity/create$', views.CreateActivity.as_view(), name='create-actiyity'),
                       url(r'^activity/update/(?P<pk>\d+)$', views.UpdateActivity.as_view(), name='update-actiyity'),
                       url(r'^activity/delete/(?P<pk>\d+)$', views.DeleteActivity.as_view(), name='delete-activiyt')
                       )