#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',

    url(r'^tag/(?P<pk>\d+)/$', views.ListNews.as_view(), name='index-sorts-news'),

)
