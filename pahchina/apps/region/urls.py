#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

import response
import views

urlpatterns = patterns('',

    #url(r'set/(?P<cate>\w+)/$', views.UserSetRegion.as_view(), name='user-update-region'),
    #url(r'update/(?P<cate>\w+)/$', views.UserSetRegion.as_view(), name='user-update-region'),

    url(r'^subcity/(?P<pk>\d+)/$', views.ListSubCity.as_view(), name='list-sub-city'),

    # response content some thing like json and so on
    url(r'^response/get/(?P<parent_id>\d+)/$', response.get_region),
    url(r'^response/city.js$', response.get_city_js),
)

