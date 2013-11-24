#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
                       url(r'^activity/list$', views.ListActivity.as_view(), name='list-activity')
                       )