#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render_to_response as r2r, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import Permission, PermissionManager, PermissionsMixin
from django.contrib.sites.models import Site, SiteManager

from .models import Website
from ..utils import SuperRequiredMixin, StaffRequiredMixin
import forms



class SiteIndex(generic.TemplateView):

    #context_object_name = 'site'
    template_name = 'site-index.html'

    def get_context_data(self, **kwargs):
        context = super(SiteIndex, self).get_context_data(**kwargs)
        context['domain'] = self.request.META['HTTP_HOST']
        return context


class DeleteSite(SuperRequiredMixin, generic.DeleteView):
    """ 创建站点详情
    第一次创建站点时调用
    """

    model = Site
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('admin-list-sites')

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk'] == "1":
            messages.error(self.request,message='总站不能被删除！')
            return HttpResponseRedirect(reverse_lazy('admin-list-sites'))
        return super(DeleteSite, self).get(self, request, *args, **kwargs)

    def post(self, *args, **kwargs):
        if self.kwargs['pk'] == "1":
            messages.error(self.request,message='总站不能被删除！')
            return HttpResponseRedirect(reverse_lazy('admin-list-sites'))
        return super(DeleteSite, self).post(*args, **kwargs)


class StaffUpdateSite(StaffRequiredMixin, generic.UpdateView):
    """ 分站管理员更新自己的站点内容
    """
    model = Site
    form_class = forms.StaffSiteForm
    template_name = 'update.html'
    success_url = reverse_lazy('admin-index')

    def get_object(self, queryset=None):
        obj = Site.objects.get(admin=self.request.user)
        return obj


class StaffDetailSite(StaffRequiredMixin, generic.TemplateView):
    """ 分站管理员更新自己的站点内容
    """
    model = Site
    template_name = 'detail-site.html'

    def get_context_data(self, **kwargs):
        context = super(StaffDetailSite, self).get_context_data(**kwargs)
        context['site'] = Site.objects.get(admin=self.request.user)
        return context