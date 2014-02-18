#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render_to_response as r2r, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import Permission, PermissionManager, PermissionsMixin
from django.contrib.sites.models import Site, SiteManager

from .models import Site
from ..utils import SuperRequiredMixin
import forms



class SiteIndex(generic.DetailView):

    context_object_name = 'site'
    slug_field = 'site_id'
    template_name = 'site-index.html'

    #def get_object(self, queryset=None):
    #    return get_current_site(self.request)
        #return Site.objects.get(id=self.kwargs['site_id'])

    #def get_context_data(self, **kwargs):
    #    context = super(SiteIndex, self).get_context_data(**kwargs)
    #    context['host'] = self.request.get_host().split(":")[0]
    #    return context

class ListSites(SuperRequiredMixin, generic.ListView):
    """ 站点列表
    """
    model = Site
    template_name = 'list-sites.html'
    context_object_name = 'site_list'


class DetailSite(SuperRequiredMixin,generic.DetailView):

    model = Site
    template_name = 'detail-site.html'


class UpdateSite(SuperRequiredMixin, generic.UpdateView):

    model = Site
    template_name = 'update.html'

    def get_success_url(self):
        return reverse('admin-detail-site', kwargs=self.kwargs)

class CreateSite(SuperRequiredMixin, generic.CreateView):
    """ 创建站点
    管理员功能
    """

    model = Site
    template_name = 'update.html'
    success_url = reverse_lazy('admin-list-site')



class DeleteSite(SuperRequiredMixin, generic.DeleteView):
    """ 创建站点详情
    第一次创建站点时调用
    """

    model = Site
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('admin-list-sites')