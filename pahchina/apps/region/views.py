#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response as r2r, get_object_or_404
from django.contrib import messages


from ..utils import LoginRequiredMixin, SuperRequiredMixin
import forms
from .models import Region, LivingRegion

class UserSetRegion(LoginRequiredMixin ,generic.FormView):

    """ 用户更新居住信息
    传入参数cate <huji, juzhu>
    传入参数为居住信息的类别，huji: 户籍所在地, juzhu: 居住地区
    """
    form_class = forms.UserUpdateRegionForm
    template_name = 'region/user-update-region.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super(UserSetRegion, self).get_context_data(**kwargs)
        cate = self.kwargs['cate']
        if cate == 'household': context['title']='修改户籍地'
        if cate == 'apartment': context['title']='修改居住地'
        return context

    def get_form_kwargs(self):
        # 传递 user, cate 到form
        kwargs = super(UserSetRegion, self).get_form_kwargs()
        # 参数非法则返回404
        if self.kwargs['cate'] not in ('apartment', 'household'): raise Http404
        kwargs.update({'user': self.request.user,
                       'cate': self.kwargs['cate'],})
        return kwargs

    def get_initial(self):
        try:
            obj = LivingRegion.objects.get(user_id=self.request.user.id, cate=self.kwargs['cate'])
            return obj.__dict__.copy()
        except LivingRegion.DoesNotExist:
            return {}

    def form_valid(self, form):
        form.save()
        messages.success(self.request, '更新信息成功！')
        return super(UserSetRegion, self).form_valid(form)


class ListSubCity(SuperRequiredMixin, generic.TemplateView):

    template_name = 'region/list-city-admin.html'

    def get_context_data(self, **kwargs):
        context = super(ListSubCity, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        if pk == '0':
            context['region'] = {'name':''}
            context['object_list'] = Region.objects.filter(parent=None)
        else:
            region = Region.objects.get(id=pk)
            context['region'] = region
            context['object_list'] = Region.objects.filter(parent=region)
        return context