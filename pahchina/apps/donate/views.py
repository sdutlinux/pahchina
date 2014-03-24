#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http.response import HttpResponseRedirect


from ...apps.donate.models import Donate, Itemized
from ..utils.views import SuperRequiredMixin, GetOr404View
from .form import DonateFormUser, ItemizedForm
from ...apps.accounts.models import User



class ListDonate(SuperRequiredMixin, generic.ListView):
    """ 列出捐赠
    """
    model = Donate
    context_object_name = 'donate_list'
    template_name = 'list-donate-admin.html'
    
    def get_queryset(self):
        order = self.request.GET.get('order')
        neg = self.request.GET.get('neg')
        _dic = {
            'date':'-create_time',
            'anyone': '-is_anonymous',
            'status': '-is_true',
            'money' : '-money',
        }
        if order in _dic:
            #parm = _dic[order] if not neg else "-{}".format(_dic[order])
            parm = _dic[order] if not neg else _dic[order][1:]
            queryset = Donate.objects.all().order_by(parm)
            return queryset
        return super(ListDonate, self).get_queryset()




class DetailDonate(SuperRequiredMixin, GetOr404View, generic.DetailView):

    model = Donate
    context_object_name = 'object_donate'
    template_name = 'detail-donate-admin.html'

    def get(self, request, *args, **kwargs):
        """ 确认到帐或者未到帐
        """
        _mark = request.GET.get('mark')
        if _mark is None:
            return super(DetailDonate, self).get(request, *args, **kwargs)
        if _mark == 'true':
            self.get_object().mark_true()
        elif _mark == 'false':
            self.get_object().mark_true(False)
        return HttpResponseRedirect(reverse('admin-detail-donate', kwargs=self.kwargs))

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(DetailDonate, self).get_context_data( **kwargs)
        donate = Donate.objects.get(id=self.kwargs['pk'])
        context['itemized_list'] = Itemized.objects.filter(donate=donate)
        return context



class CreateDonate(SuperRequiredMixin, generic.CreateView):
    model = Donate
    success_url = reverse_lazy('admin-list-donate')
    template_name = 'update-donate-admin.html'


class UpdateDonate(SuperRequiredMixin, generic.UpdateView):

    model = Donate
    template_name = 'update-donate-admin.html'
    def get_success_url(self):
        return reverse('admin-detail-donate',kwargs=self.kwargs)


class DeleteDonate(SuperRequiredMixin, generic.DeleteView):
    model = Donate
    success_url = reverse_lazy('admin-list-donate')
    template_name = 'confirm_delete.html'


class CreateDonateUser(generic.FormView):
    """ 用户创建捐赠
    """
    form_class = DonateFormUser
    template_name = 'create-donate.html'
    success_url = reverse_lazy('list-donate')

    def get_form_kwargs(self):
        kwargs = super(CreateDonateUser, self).get_form_kwargs()
        if self.request.user.is_authenticated():
            kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CreateDonateUser, self).form_valid(form)

class ListDonateUser(generic.DetailView):
    model = User
    template_name = 'list-donate.html'

    def get_context_data(self, **kwargs):
        context = super(ListDonateUser, self).get_context_data( **kwargs)
        context['donate_list'] = Donate.objects.filter(user=self.request.user).order_by('-create_time')
        return  context

    def get_object(self, queryset=None):
        return self.request.user

class DetailDonateUser(GetOr404View, generic.DetailView):
    """ 用户查看自己的某一条捐赠记录
    以及该捐赠的使用详情
    """
    model = Donate
    context_object_name = 'object_donate'
    template_name = 'detail-donate.html'

    def get_context_data(self, **kwargs):
        context = super(DetailDonateUser, self).get_context_data( **kwargs)
        donate = Donate.objects.get(id=self.kwargs['pk'])
        context['itemized_list'] = Itemized.objects.filter(donate=donate)
        return context

#class ListItemizedId(SuperRequiredMixin, generic.DetailView):
#
#    model = Donate
#    template_name = 'list-itemized-admin.html'
#
#    def get_context_data(self, **kwargs):
#        context = super(ListItemizedId, self).get_context_data( **kwargs)
#        donate = Donate.objects.get(id=self.kwargs['pk'])
#        context['itemized_list'] = Itemized.objects.filter(number=donate)
#        return context



class ListItemized(SuperRequiredMixin, generic.ListView):
    """ 使用记录列表
    暂无使用
    """
    model = Itemized
    context_object_name = 'itemized_list'
    template_name = 'list-itemized-admin.html'



class DetailItemized(SuperRequiredMixin, generic.DetailView):
    """ 查看使用记录
    暂无使用
    """
    model = Itemized
    context_object_name = 'object_itemized'
    template_name = 'detail-itemized-admin.html'


class CreateItemizedId(generic.CreateView):
    """ 创建捐赠使用记录
    两种使用方法，实际页面和弹出页面
    """
    model = Itemized
    form_class = ItemizedForm
    template_name = 'update-itemized-admin.html'

    def get_success_url(self):
        return reverse('admin-detail-donate', kwargs=self.kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateItemizedId, self).get_form_kwargs()
        kwargs['donate'] = Donate.objects.get(id = self.kwargs["pk"])
        kwargs['user'] = self.request.user
        return kwargs

class UpdateItemized(SuperRequiredMixin, generic.UpdateView):

    model = Itemized
    form_class = ItemizedForm
    template_name = 'update-itemized-admin.html'
    
    def get_form_kwargs(self):
        kwargs = super(UpdateItemized, self).get_form_kwargs()
        kwargs['donate'] = self.object.donate
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):

        return reverse('admin-detail-donate', kwargs={'pk': self.get_object().donate.id})


class DeleteItemized(SuperRequiredMixin, generic.DeleteView):

    model = Itemized
    success_url = reverse_lazy('admin-list-itemized')
    context_object_name = 'object'
    template_name = 'confirm_delete.html'

    def get_success_url(self):

        return reverse('admin-detail-donate', kwargs={'pk': self.object.donate.id})