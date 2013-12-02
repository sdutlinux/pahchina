#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from ..utils import SuperUser
from ..patient.models import Patient

from .models import Hospital, Doctor, Record
from .forms import UpdateHospitalForm, RecordForm


class HospitalProfile(generic.DetailView):
    """ 医院用户登录成功页面
    """
    context_object_name = 'hospital'
    template_name = 'profile-hospital.html'

    def get_object(self, queryset=None):
        return self.request.user.hospital


class UpdateHospitalProfile(generic.UpdateView):

    form_class = UpdateHospitalForm
    success_url = reverse_lazy('profile-hospital')
    template_name = 'update-user-profile.html'

    def get_object(self, queryset=None):
        return self.request.user.hospital


class ListHospital(generic.ListView, SuperUser):
    """ 列出所有医院
    """
    model = Hospital
    template_name = 'list-hospital.html'

class DetailHospital(generic.DetailView, SuperUser):
    """ 管理员查看医院详细信息
    """
    model = Hospital
    context_object_name = 'hospital'
    template_name = 'detail-hospital.html'

class UpdateHospital(generic.UpdateView, SuperUser):
    """ 管理员更新医院信息
    """
    model = Hospital
    success_url = reverse_lazy('admin-list-hospital')
    template_name = 'update.html'


class DeleteHospital(generic.DeleteView, SuperUser):
    """ 管理员删除医院
    """
    model = Hospital
    success_url = reverse_lazy('admin-list-hospital')
    template_name = 'confirm_delete.html'


class DetailDoctor(generic.DetailView, SuperUser):
    """ 医生查看医生详情
    """
    model = Doctor
    context_object_name = 'doctor'
    template_name = 'detail-doctor.html'

class ListDoctor(generic.ListView, SuperUser):
    """ 管理员列出所有医生
    """
    model = Doctor
    template_name = 'list-doctor.html'

class UpdateDoctor(generic.UpdateView, SuperUser):
    """ 管理员更新医生信息
    """
    model = Doctor
    success_url = reverse_lazy('admin-list-doctor')
    template_name = 'update.html'

    def get_success_url(self):
        return reverse('admin-detail-doctor', kwargs=self.kwargs)


class CreateRecord(generic.FormView):
    """ 管理员或者医生用开给患者创建病历
    """
    form_class = RecordForm
    template_name = 'update.html'

    def get_form_kwargs(self):
        kwargs = super(CreateRecord, self).get_form_kwargs()
        kwargs['patient'] = get_object_or_404(Patient, id=self.kwargs['pk'])
        return kwargs

    def get_success_url(self):
        return reverse('admin-detail-patient', kwargs=self.kwargs)
    
    def form_valid(self, form):
        form.save()
        return super(CreateRecord, self).form_valid(form)

class ListRecord(generic.DetailView, SuperUser):
    """ 管理员查看患者所有病例
    """

    model = Patient
    context_object_name = 'patient'
    template_name = 'list-record.html'

    def get_context_data(self, **kwargs):
        context = super(ListRecord, self).get_context_data( **kwargs)
        context['record_list'] = Record.objects.filter(patient_id = self.kwargs['pk'])
        return context

class DetailRecord(generic.DetailView, SuperUser):
    """ 管理员查病历详情
    """
    model = Record
    context_object_name = 'record'
    template_name = 'detail-record-admin.html'

    def get_context_data(self, **kwargs):
        context = super(DetailRecord, self).get_context_data( **kwargs)
        context['patient'] = get_object_or_404(Patient, id=self.kwargs['patient'])
        return context

class DeleteRecord(generic.DeleteView, SuperUser):
    """ 管理员删除病历
    """
    model = Record
    context_object_name = 'object'
    template_name = 'confirm_delete.html'



