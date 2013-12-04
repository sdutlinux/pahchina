#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_reset
from django.core.urlresolvers import reverse_lazy, reverse

from . import views


urlpatterns = patterns('',

    url(r'^$', views.admin_index, name='admin-index'),

    url(r'^login/$', views.pah_login, name='login'),
    url(r'^register/$', views.pah_register, name='register'),
    url(r'^logout$', views.pah_logout, name='logout'),

    url(r'^profile/$', views.Profile.as_view(), name='profile'),
    url(r'^show/(?P<pk>\d+)/$', views.Show.as_view(), name='profile'),

    url(r'^profile/update/$', views.UpdateProfile.as_view(), name='update-profile'),
    #url(r'^password/update/$', views.change_password, name='update-password'),
    url(r'^password/update/$', views.UpdatePassword.as_view(), name='update-password'),

    url(r'^user/list$', views.ListUser.as_view(), name='admin-list-user'),
    url(r'^admin/user/create/$', views.CreateUser.as_view(), name='admin-create-user'),
    url(r'^admin/user/(?P<pk>\d+)/$', views.DetailUser.as_view(), name='admin-detail-user'),

    url(r'^admin/user/update/(?P<pk>\d+)/$', views.UpdateUser.as_view(), name='admin-update-user'),

    url(r'^admin/user/update/identity/(?P<pk>\d+)/$', views.UpdateIdentity.as_view(), name='admin-update-identity'),

    url(r'^admin/user/delete/(?P<pk>\d+)/$', views.DeleteUser.as_view(), name='admin-delete-user'),
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
