#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render_to_response as r2r, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm

from .models import Patient, Drug, Dosage
from .forms import UpdatePatientForm, CreateDosageForm
from ..utils import SuperUser

class DetailPatient(generic.DeleteView):
    """ 管理员查看患者信息
    """
    model = Patient
    context_object_name = 'patient'
    template_name = 'detail-patient.html'

class ListPatient(generic.ListView, SuperUser):
    """ 管理员查看患者列表
    """
    model = Patient
    context_object_name = 'patient_list'
    template_name = 'list-patient.html'

class UpdatePatient(generic.UpdateView, SuperUser):
    """ 管理员更新患者信息
    """
    model = Patient
    form_class = UpdatePatientForm
    template_name = 'update-patient.html'

    def get_success_url(self):
        return reverse('admin-detail-patient', kwargs=self.kwargs)

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
    """
    form_class = UpdatePatientForm
    success_url = reverse_lazy('profile-patient')
    template_name = 'update-user-profile.html'

    def get_object(self, queryset=None):
        return self.request.user.patient

class ListDrug(generic.ListView, SuperUser):
    """ 药物列表
    """
    model = Drug
    context_object_name = 'drug_list'
    template_name = 'list-drug.html'

class CreateDrug(generic.CreateView, SuperUser):
    """ 添加药物
    """
    model = Drug
    success_url = reverse_lazy('admin-list-drug')
    template_name = 'update.html'

class UpdateDrug(generic.UpdateView, SuperUser):
    """ 修改
    """
    model = Drug
    success_url = reverse_lazy('admin-list-drug')
    template_name = 'update.html'

class DeleteDrug(generic.DeleteView, SuperUser):
    """ 删除药物
    """
    model = Drug
    #context_object_name = 'object'
    success_url = reverse_lazy('admin-list-drug')
    template_name = 'confirm_delete.html'

class ListDosage(generic.ListView, SuperUser):
    """ 使用剂量列表
    """
    model = Dosage
    context_object_name = 'dosage_list'
    template_name = 'list-dosage.html'

class DetailPatientDosage(generic.DetailView, SuperUser):

    model = Patient
    context_object_name = 'patient'
    template_name = 'detail-patient-dosage.html'

    def get_context_data(self, **kwargs):
        context = super(DetailPatientDosage, self).get_context_data( **kwargs)
        context['dosage_list'] = Dosage.objects.filter(patient_id = self.kwargs['pk'])
        return context

class DetailOwnDosage(generic.DetailView):
    """ 患者查看个人用药记录
    """
    context_object_name = 'dosage_list'
    template_name = 'detail-dosage.html'

    def get_object(self, queryset=None):
        return Dosage.objects.filter(patient=self.request.user.patient)

class CreateOwnDosage(generic.FormView):
    """ 患者创建个人用药记录
    """

    form_class = CreateDosageForm
    success_url = reverse_lazy('detail-dosage')
    template_name = 'update-user-profile.html'

    def get_form_kwargs(self):
        kwargs = super(CreateOwnDosage, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(CreateOwnDosage, self).form_valid(form)


class CreateDosage(generic.CreateView, SuperUser):
    """ 管理员创建患者用药记录
    """
    model = Dosage
    success_url = reverse_lazy('admin-list-dosage')
    template_name = 'update.html'

class UpdateDosage(generic.UpdateView, SuperUser):
    """ 管理员修改患者用药记录
    """
    model = Dosage
    success_url = reverse_lazy('admin-list-dosage')
    template_name = 'update.html'
