#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',

    url(r'^$', views.SiteIndex.as_view(), name='site-index'),

    url(r'^regions/(?P<pk>\d+)/$', views.RegionWebsite.as_view(), name='set-site-region'),

    url(r'^create/$', views.CreateSite.as_view(), name='admin-create-website'),

    # 站点管理员功能
    url(r'^detail/site/$', views.StaffDetailSite.as_view(), name='staff-detail-mysite'),
    url(r'^update/site/$', views.StaffUpdateSite.as_view(), name='staff-update-mysite'),
    url(r'^my/users/$', views.WebsiteListUsers.as_view(), name='staff-list-users'),
    ## 站点管理员操作友情链接
    url(r'^links/list/$', views.ListMyFriLink.as_view(), name='staff-list-links'),
    url(r'^links/create/$', views.CreateMyFriLink.as_view(), name='staff-create-links'),
    url(r'^links/delete/(?P<pk>\d+)/$', views.DeleteMyFreLink.as_view(), name='staff-delete-links'),

)

