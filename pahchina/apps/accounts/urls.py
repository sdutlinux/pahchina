#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_reset
from django.core.urlresolvers import reverse_lazy, reverse

from . import views


urlpatterns = patterns('',

    url(r'^login/$', views.pah_login, name='login'),
    url(r'^register/$', views.pah_register, name='register'),
    url(r'^logout$', views.pah_logout, name='logout'),

    url(r'^profile/update/$', views.UpdateProfile.as_view(), name='update-profile'),

    #url(r'^password/reset/$', password_reset, {'template_name':'password_reset_form.html'}, name='password-reset'),

    url(r'^$', views.admin_index, name='admin-index'),

    url(r'^user/list$', views.ListUser.as_view(), name='list-user'),
    url(r'^user/create$', views.CreateUser.as_view(), name='create-user'),
    url(r'^user/(?P<pk>\d+)$', views.DetailUser.as_view(), name='detail-user'),

    url(r'^user/update/(?P<pk>\d+)$', views.UpdateUser.as_view(), name='update-user'),
    url(r'^user/update/(?P<pk>\d+)/password$', views.ListUser.as_view(), name='update-user-password'),

    url(r'^user/delete/(?P<pk>\d+)$', views.DeleteUser.as_view(), name='delete-user'),
)

urlpatterns += patterns('',

    url(r'^user/password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/accounts/user/password/reset/done/',},
        name="password-reset"),

    url(r'^user/password/reset/done/$', 'django.contrib.auth.views.password_reset_done',
        name='password-reset-done'),

    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/accounts/user/password/done/'}),

    url(r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete', name='password-reset-complete'),
)
