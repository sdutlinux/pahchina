#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',

    url(r'^hospital/profile/update$', views.UpdateHospitalProfile.as_view(), name='update-hospital'),

    url(r'^doctor/update/profile/$', views.DoctorUpdateProfile.as_view(), name='doctor-update-profile'),

    url(r'^doctor/patients/$', views.MyPatient.as_view(), name='doctor-list-patient'),
    url(r'^hospital/doctors/$', views.ListDoctor.as_view(), name='hospital-list-doctor'),

    url(r'^hospital/list/doctors/(?P<pk>\d+)/$', views.ListDoctorPatient.as_view(),
        name='hospital-list-doctor-patient'),


    url(r'^admin/list/doctors/(?P<pk>\d+)/$', views.ListDoctorPatient.as_view(),
        name='admin-list-doctor-patient'), # 管理员查看该医生的病人

    url(r'^record/create/(?P<pk>\d+)/$', views.CreateRecord.as_view(), name='create-record'),
    url(r'^record/list/(?P<pk>\d+)/$', views.ListRecord.as_view(),
        name='admin-list-record'),
    url(r'^admin/record/delete/(?P<pk>\d+)/$', views.DeleteRecord.as_view(),
        name='admin-delete-record'),
    url(r'^admin/record/detail/(?P<patient>\d+)/(?P<pk>\d+)/$', views.DetailRecord.as_view(),
        name='admin-detail-record'),


    url(r'^doctor/record/list/(?P<pk>\d+)/$', views.ListDoctorRecord.as_view(),
        name='list-doctor-record'),
    url(r'^admin/doctor/record/detail/(?P<pk>\d+)/$', views.DetailDoctorRecord.as_view(),
        name='admin-detail-doctor-record'),
    url(r'^admin/doctor/record/start/(?P<pk>\d+)/$', views.StartDoctorRecord.as_view(),
        name='admin-start-doctor-record'),
    url(r'^admin/doctor/record/end/(?P<pk>\d+)/$', views.EndDoctorRecord.as_view(),
        name='admin-end-doctor-record'),
    url(r'^admin/doctor/record/update/(?P<pk>\d+)/$', views.UpdateDoctorRecord.as_view(),
        name='admin-update-doctor-record'),

    url(r'^patient/doctor/record/list/$', views.ListDoctorRecord.as_view(),
        name='patient-list-doctor-record'),
    url(r'^patient/doctor/record/detail/(?P<pk>\d+)/$', views.DetailDoctorRecord.as_view(),
        name='patient-detail-doctor-record'),
    url(r'^patient/doctor/record/start/$', views.StartDoctorRecord.as_view(),
        name='patient-start-doctor-record'),
    url(r'^patient/doctor/record/end/(?P<pk>\d+)/$', views.EndDoctorRecord.as_view(),
        name='patient-end-doctor-record'),
)
