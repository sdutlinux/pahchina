#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^admin/list/$', views.ListNews.as_view(), name='admin-list-news'),
                       url(r'^admin/(?P<pk>\d+)/$', views.DetailNews.as_view(), name='admin-detail-news'),
                       url(r'^(?P<pk>\d+)/$', views.DetailNewsUser.as_view(), name='detail-news'),
                       url(r'^admin/create/$', views.CreateNews.as_view(), name='admin-create-news'),
                       url(r'^admin/update/(?P<pk>\d+)/$', views.UpdateNews.as_view(), name='admin-update-news'),
                       url(r'^admin/delete/(?P<pk>\d+)/$', views.DeleteNews.as_view(), name='admin-delete-news'),
                       
                       url(r'^admin/sorts/list$', views.ListSorts.as_view(), name='admin-list-sorts'),
                       url(r'^admin/sorts/(?P<pk>\d+)$', views.DetailSorts.as_view(), name='admin-detail-sorts'),
                       url(r'^admin/sorts/create$', views.CreateSorts.as_view(), name='admin-create-sorts'),
                       url(r'^admin/sorts/update/(?P<pk>\d+)$', views.UpdateSorts.as_view(), name='admin-update-sorts'),
                       url(r'^admin/sorts/delete/(?P<pk>\d+)$', views.DeleteSorts.as_view(), name='admin-delete-sorts'),
                       )