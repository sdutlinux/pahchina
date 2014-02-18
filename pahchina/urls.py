#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# 同步创建相关身份
from .apps.utils import OnCreate

from .apps.index import views


urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^about/$', views.About.as_view(), name='about'),

    # url(r'^pahchina/', include('pahchina.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # include accounts
    url(r'^accounts/', include('pahchina.apps.accounts.urls')),
    url(r'^patients/', include('pahchina.apps.patient.urls')),
    url(r'^activity/', include('pahchina.apps.activity.urls')),
    url(r'^volunteer/', include('pahchina.apps.volunteer.urls')),
    url(r'^donate/', include('pahchina.apps.donate.urls')),
    url(r'^medical/', include('pahchina.apps.medical.urls')),
    url(r'^site/', include('pahchina.apps.subsites.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

