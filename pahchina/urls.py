#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    #url(r'^$', '', name='index'),

    # url(r'^pahchina/', include('pahchina.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^ueditor/',include('DjangoUeditor.urls' )), # 富文本编辑器
    # include accounts
    url(r'^accounts/', include('pahchina.apps.accounts.urls'))
)
