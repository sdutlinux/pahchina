#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
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

from .models import Website, Links
from ..region.models import Region
from ..utils import SuperRequiredMixin, StaffRequiredMixin
import forms
from .utils import get_my_users

class SiteIndex(generic.TemplateView):

    template_name = 'site-index.html'

    def get_context_data(self, **kwargs):
        context = super(SiteIndex, self).get_context_data(**kwargs)
        context['domain'] = self.request.META['HTTP_HOST']
        return context

class CreateSite(SuperRequiredMixin, generic.CreateView):
    """ 管理员创建站点
    自定义了form, 限制站长为站点管理员， 即： is_staff
    """
    model = Website
    form_class = forms.CreateSiteForm
    template_name = 'admin-update.html'

    def get_success_url(self):
        return reverse('admin-list', kwargs={'model':'website'})

    def get_context_data(self, **kwargs):
        context = super(CreateSite, self).get_context_data(**kwargs)
        context['title'] = '创建站点'
        return context

class StaffUpdateSite(StaffRequiredMixin, generic.UpdateView):
    """ 分站管理员更新自己的站点内容
    """
    model = Website
    form_class = forms.StaffSiteForm
    template_name = 'admin-update.html'
    success_url = reverse_lazy('admin-index')

    def get_context_data(self, **kwargs):
        context = super(StaffUpdateSite, self).get_context_data(**kwargs)
        context['title'] = '修改我的站点'
        return context

    def get_object(self, queryset=None):
        obj = Website.objects.get(admin=self.request.user)
        return obj


class StaffDetailSite(StaffRequiredMixin, generic.TemplateView):
    """ 分站管理员更新自己的站点内容
    """
    model = Website
    template_name = 'detail-site.html'

    def get_context_data(self, **kwargs):
        context = super(StaffDetailSite, self).get_context_data(**kwargs)
        context['site'] = Website.objects.get(admin=self.request.user)
        return context


class RegionWebsite(generic.UpdateView):
    """ 更改分站所包含的城市
    """
    model = Website
    form_class = forms.RegionWebsiteForm
    template_name = 'admin-update.html'
    
    def get_object(self, queryset=None):
        if self.kwargs['pk'] == '1':
            raise Http404
        else:
            return super(RegionWebsite, self).get_object(queryset=None)

    def get_context_data(self, **kwargs):
        context = super(RegionWebsite, self).get_context_data(**kwargs)
        context['title'] = u'[{}] 包含的城市'.format(self.object.name)
        return context

    def get_initial(self):
        initial_data = super(RegionWebsite, self).get_initial()
        #initial_data['regions'] = self.object.region_set
        return initial_data

    def get_success_url(self):
        return reverse('set-site-region', kwargs=self.kwargs)

class WebsiteListUsers(generic.TemplateView):

    #model = Website
    template_name = 'website/list-user.html'

    def get_context_data(self, **kwargs):
        context = super(WebsiteListUsers, self).get_context_data(**kwargs)
        website = Website.objects.get(admin=self.request.user)
        context['user_list'] = get_my_users(website)
        return context

# 友情链接相关，普通站点管理员修改分站的友情链接
# 管理员修改主站的友情链接
class ListMyFriLink(StaffRequiredMixin, generic.ListView):

    model = Links

    def get_queryset(self):
        queryset = Links.objects.filter(site=self.request.user.website)
        return queryset

class CreateMyFriLink(StaffRequiredMixin, generic.FormView):

    model = Links
    form_class = forms.MyFreLinkForm
    success_url = reverse_lazy('staff-list-links')
    template_name = 'admin-update.html'

    def get_context_data(self, **kwargs):
        con = super(CreateMyFriLink, self).get_context_data(**kwargs)
        con['title'] = "创建友情链接"
        return con

    def get_form_kwargs(self):
        kwargs = super(CreateMyFriLink, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CreateMyFriLink, self).form_valid(form)

class DeleteMyFreLink(StaffRequiredMixin, generic.DeleteView):

    model = Links
    success_url = reverse_lazy('staff-list-links')
    template_name = 'confirm_delete.html'

    def get_object(self, queryset=None):
        # 判断是否是当前用户的站点
        obj = super(DeleteMyFreLink, self).get_object()
        if obj.website != self.request.user.website:
            raise Http404
        return obj