#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',

    url(r'^$', views.SiteIndex.as_view(), name='site-index'),
    #url(r'(?P<site_id>\d+)/$', views.SiteIndex.as_view(), name='site-index'),



    url(r'^admin/create/site$', views.CreateSite.as_view(), name='admin-create-site'),
    url(r'^admin/list$', views.ListSites.as_view(), name='admin-list-sites'),
    url(r'^admin/detail/(?P<pk>\d+)/$', views.DetailSite.as_view(), name='admin-detail-site'),
    url(r'^admin/update/(?P<pk>\d+)/$', views.UpdateSite.as_view(), name='admin-update-site'),
    url(r'^admin/update/(?P<pk>\d+)/$', views.DeleteSite.as_view(), name='admin-delete-site'),

)

