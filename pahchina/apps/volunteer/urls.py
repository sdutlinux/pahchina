#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
                       url(r'^admin/list/$', views.ListVolunteer.as_view(), name='admin-list-volunteer'),
                       url(r'^admin/(?P<pk>\d+)/$', views.DetailVolunteer.as_view(), name='admin-detail-volunteer'),
                       url(r'^admin/create/$', views.CreateVolunteer.as_view(), name='admin-create-volunteer'),
                       url(r'^admin/update/(?P<pk>\d+)/$', views.UpdateVolunteer.as_view(), name='admin-update-volunteer'),
                       url(r'^admin/delete/(?P<pk>\d+)/$', views.DeleteVolunteer.as_view(), name='admin-delete-volunteer')
                       )