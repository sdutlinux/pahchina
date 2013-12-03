#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',

    #url(r'^profile/$', views.Profile.as_view(), name='profile-patient'),
    url(r'^hospital/profile/$', views.HospitalProfile.as_view(), name='profile-hospital'),
    url(r'^hospital/profile/update$', views.UpdateHospitalProfile.as_view(), name='update-hospital'),

    url(r'^admin/hospital/list/$', views.ListHospital.as_view(), name='admin-list-hospital'),
    url(r'^admin/hospital/detail/(?P<pk>\d+)/$', views.DetailHospital.as_view(), name='admin-detail-hospital'),
    url(r'^admin/hospital/update/(?P<pk>\d+)/$', views.UpdateHospital.as_view(), name='admin-update-hospital'),

    url(r'^admin/doctor/list/$', views.ListDoctor.as_view(), name='admin-list-doctor'),
    url(r'^admin/doctor/detail/(?P<pk>\d+)/$', views.DetailDoctor.as_view(), name='admin-detail-doctor'),
    url(r'^admin/doctor/update/(?P<pk>\d+)/$', views.UpdateDoctor.as_view(), name='admin-update-doctor'),

    url(r'^record/create/(?P<pk>\d+)/$', views.CreateRecord.as_view(), name='create-record'),
    url(r'^record/list/(?P<pk>\d+)/$', views.ListRecord.as_view(), name='admin-list-record'),
    url(r'^admin/record/delete/(?P<pk>\d+)/$', views.DeleteRecord.as_view(), name='admin-delete-record'),
    url(r'^admin/record/detail/(?P<patient>\d+)/(?P<pk>\d+)/$', views.DetailRecord.as_view(), name='admin-detail-record'),
)
