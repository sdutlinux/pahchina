#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf.urls import patterns, include, url


from . import views


urlpatterns = patterns('',

    url(r'^list/$', views.ListPatient.as_view(), name='list-patient'),
    url(r'^detail/(?P<pk>\d+)/$', views.DetailPatient.as_view(), name='detail-patient'),
    url(r'^update/(?P<pk>\d+)/$', views.UpdatePatient.as_view(), name='update-patient'),

)
