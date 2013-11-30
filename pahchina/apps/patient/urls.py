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


    url(r'^admin/drug/list/$', views.ListDrug.as_view(), name='admin-list-drug'),
    url(r'^admin/drug/create/$', views.CreateDrug.as_view(), name='admin-create-drug'),
    url(r'^admin/drug/update/(?P<pk>\d+)/$', views.UpdateDrug.as_view(), name='admin-update-drug'),
    url(r'^admin/drug/delete/(?P<pk>\d+)/$', views.DeleteDrug.as_view(), name='admin-delete-drug'),

    url(r'^admin/dosage/detail/patient/(?P<pk>\d+)/$', views.DeleteDrug.as_view(),
        name='admin-detail-patient-dosage'),

    url(r'^dosage/detail/$', views.DetailOwnDosage.as_view(), name='detail-dosage'),
    url(r'^dosage/create/$', views.CreateOwnDosage.as_view(), name='create-dosage'),

    url(r'^admin/dosage/list/$', views.ListDosage.as_view(), name='admin-list-dosage'),
    url(r'^admin/dosage/detail/(?P<pk>\d+)/$', views.DetailPatientDosage.as_view(),
        name='admin-detail-patient-dosage'),
    url(r'^admin/dosage/create/$', views.CreateDosage.as_view(), name='admin-create-dosage'),
    url(r'^admin/dosage/update/(?P<pk>\d+)/$', views.UpdateDosage.as_view(), name='admin-update-dosage'),

)
