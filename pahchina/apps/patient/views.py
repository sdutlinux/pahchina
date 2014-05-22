#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render_to_response as r2r, get_object_or_404

from .models import Patient, Drug, Dosage
import forms
from .forms import UpdatePatientForm, CreateDosageForm, AdminCreateDosageForm
from ..utils import SuperRequiredMixin



class Profile(generic.DetailView):
    """ 患者用来查看个人信息
    """
    template_name = 'profile-patient.html'

    def get_object(self, queryset=None):
        try:
            return self.request.user.patient
        except:
            raise Http404

class UpdateProfile(generic.UpdateView):
    """ 患者更新个人信息
    患者用来更新个人患者基础信息
    """
    form_class = UpdatePatientForm
    success_url = reverse_lazy('profile-patient')
    template_name = 'update-user-profile.html'

    def get_object(self, queryset=None):
        return self.request.user.patient


class ListDosage(SuperRequiredMixin, generic.ListView):
    """ 使用剂量列表
    管理员使用
    用来查看所有患者的用药记录，这里只用时间的先后，不区分患者
    测试功能，后期可能用来统计数据或者其他操作
    """
    model = Dosage
    context_object_name = 'dosage_list'
    template_name = 'list-dosage.html'

class DetailPatientDosage(SuperRequiredMixin, generic.DetailView):
    """ 患者用药详情页面
    管理员用来查看患者在那个时间段用了什么药，药量是多少等
    """
    model = Patient
    context_object_name = 'patient'
    template_name = 'detail-patient-dosage.html'

    def get_context_data(self, **kwargs):
        context = super(DetailPatientDosage, self).get_context_data( **kwargs)
        context['dosage_list'] = Dosage.objects.filter(patient_id = self.kwargs['pk'])
        return context

class DetailOwnDosage(generic.DetailView):
    """ 患者查看个人用药记录
    患者在登录后查看自己的用药记录
    """
    context_object_name = 'dosage_list'
    template_name = 'detail-dosage.html'

    def get_object(self, queryset=None):
        return Dosage.objects.filter(patient=self.request.user.patient)

class CreateOwnDosage(generic.FormView):
    """ 患者创建个人用药记录
    患者在登录后创建自己的用药记录
    """

    form_class = CreateDosageForm
    success_url = reverse_lazy('detail-dosage')
    template_name = 'update-user-profile.html'

    def get_form_kwargs(self):
        kwargs = super(CreateOwnDosage, self).get_form_kwargs()
        kwargs['patient'] = self.request.user.patient
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CreateOwnDosage, self).form_valid(form)


class CreateDosage(SuperRequiredMixin, generic.FormView):
    """ 管理员创建患者用药记录
    """
    model = Dosage
    form_class = CreateDosageForm
    template_name = 'admin-update.html'

    def get_success_url(self):
        return reverse('admin-detail-patient-dosage', kwargs=self.kwargs)
    
    def get_form_kwargs(self):
        kwargs = super(CreateDosage, self).get_form_kwargs()
        kwargs['patient'] = get_object_or_404(Patient, id=self.kwargs['pk'])
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CreateDosage, self).form_valid(form)

class UpdateDosage(SuperRequiredMixin, generic.UpdateView):
    """ 管理员修改患者用药记录
    """
    model = Dosage
    success_url = reverse_lazy('admin-list-dosage')
    template_name = 'admin-update.html'
