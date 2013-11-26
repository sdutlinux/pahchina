#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf.urls import patterns, include, url


from . import views


urlpatterns = patterns('',

    url(r'^profile/$', views.Profile.as_view(), name='profile-patient'),

    url(r'^profile/update/$', views.UpdateProfile.as_view(), name='update-patient-profile'),

    url(r'^admin/list/$', views.ListPatient.as_view(), name='admin-list-patient'),
    url(r'^admin/detail/(?P<pk>\d+)/$', views.DetailPatient.as_view(), name='admin-detail-patient'),
    url(r'^admin/update/(?P<pk>\d+)/$', views.UpdatePatient.as_view(), name='admin-update-patient'),

)
