#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
                       url(r'^volunteer/list$', views.ListVolunteer.as_view(), name='list-volunteer'),
                       url(r'^volunteer/(?P<pk>\d+)$', views.DetailVolunteer.as_view(), name='detail-volunteer'),
                       url(r'^volunteer/create$', views.CreateVolunteer.as_view(), name='create-volunteer'),
                       url(r'^volunteer/update/(?P<pk>\d+)$', views.UpdateVolunteer.as_view(), name='update-volunteer'),
                       url(r'^volunteer/delete/(?P<pk>\d+)$', views.DeleteVolunteer.as_view(), name='delete-volunteer')
                       )