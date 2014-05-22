#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect

from ..utils import SuperUser, SuperRequiredMixin, LoginRequiredMixin
from ..patient.models import Patient

from .models import Hospital, Doctor, Record, DoctorRecord
#from .forms import UpdateHospitalForm, RecordForm, \
#    DoctorRecordStartForm, DoctorRecordEndForm
import forms

class UpdateHospitalProfile(LoginRequiredMixin, generic.UpdateView):
    """ 更新医院信息，管理员和医院通用
    """
    model = Hospital
    form_class = forms.UpdateHospitalForm
    success_url = reverse_lazy('admin-list-hospital')
    template_name = 'update-user-profile.html'

    def get_object(self, queryset=None):
        self.object = self.request.user.hospital
        return self.object


class ListDoctor(LoginRequiredMixin, generic.ListView):
    """ 管理员列出所有医生
    """
    model = Doctor
    template_name = 'list-doctor.html'

    def get_queryset(self):
        if self.request.user.is_hospital:
            return self.request.user.hospital.doctor_set.all()
        else:
            raise Http404

class ListDoctorPatient(LoginRequiredMixin, generic.DetailView):
    """ 查看该医生的病人
    使用者： 管理员、医院
    """
    model = Doctor

    def get_template_names(self):
        if self.request.user.is_hospital:
            return 'list-my-patient.html'
        elif self.request.user.is_superuser:
            return 'list-patient.html'

    def get_context_data(self, **kwargs):
        context = super(ListDoctorPatient, self).get_context_data(**kwargs)
        if self.request.user.is_hospital and \
            self.get_object().hospital == self.request.user.hospital or \
                self.request.user.is_superuser:
            context['patient_list'] = self.get_object().get_patients()
        return context

class DoctorUpdateProfile(generic.UpdateView):
    """ 医生更新医生信息
    """
    model = Doctor
    form_class = forms.UpdateDoctorForm
    template_name = 'index-update.html'

    def get_object(self, queryset=None):
        return Doctor.objects.get(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(DoctorUpdateProfile, self).get_context_data(**kwargs)
        context['title'] = '修改医生信息'
        return context

    def get_success_url(self):
        return reverse('profile')



class MyPatient(LoginRequiredMixin, generic.ListView):
    """ 医生或者医院查看自己的病人
    """

    template_name = 'list-my-patient.html'
    context_object_name = 'patient_list'

    def get_queryset(self):
        if self.request.user.is_doctor:
            records = DoctorRecord.objects.filter(end_date=None,
                      doctor=self.request.user.doctor).order_by('from_date')
        elif self.request.user.is_hospital:
            doctors = self.request.user.hospital.doctor_set.all()
            records = []
            for d in doctors:
                records += DoctorRecord.objects.filter(end_date=None, doctor=d)
        else:
            return HttpResponseRedirect(reverse_lazy('index'))
        patient_list = [p.patient for p in records]
        return patient_list


class CreateRecord(LoginRequiredMixin, generic.FormView):
    """ 管理员或者医生用开给患者创建病历
    """
    form_class = forms.RecordForm
    template_name = 'admin-update.html'

    def get_form_kwargs(self):
        kwargs = super(CreateRecord, self).get_form_kwargs()
        kwargs['patient'] = get_object_or_404(Patient, id=self.kwargs['pk'])
        return kwargs

    def get_success_url(self):
        self.kwargs['model']='patient'
        return reverse('admin-detail', kwargs=self.kwargs)
    
    def form_valid(self, form):
        form.save()
        return super(CreateRecord, self).form_valid(form)

class ListRecord(SuperRequiredMixin, generic.DetailView):
    """ 管理员查看患者所有病例
    """

    model = Patient
    context_object_name = 'patient'
    template_name = 'list-record.html'

    def get_context_data(self, **kwargs):
        context = super(ListRecord, self).get_context_data( **kwargs)
        context['record_list'] = Record.objects.filter(patient_id = self.kwargs['pk'])
        return context

class DetailRecord(SuperRequiredMixin, generic.DetailView):
    """ 管理员查病历详情
    """
    model = Record
    context_object_name = 'record'
    template_name = 'detail-record-admin.html'

    def get_context_data(self, **kwargs):
        context = super(DetailRecord, self).get_context_data( **kwargs)
        context['patient'] = get_object_or_404(Patient, id=self.kwargs['patient'])
        return context

class DeleteRecord(SuperRequiredMixin, generic.DeleteView):
    """ 管理员删除病历
    """
    model = Record
    context_object_name = 'object'
    template_name = 'confirm_delete.html'

class ListDoctorRecord(LoginRequiredMixin, generic.DetailView):
    """ 管理员查看患者就医记录
    查看患者曾经被那些医生治疗过
    """

    model = Patient
    context_object_name = 'patient'
    #template_name = 'list-doctor-record-admin.html'

    def get_object(self, queryset=None):
        if self.request.user.is_superuser:
            return super(ListDoctorRecord, self).get_object()
        elif self.request.user.is_patient:
            return self.request.user.patient
        else:
            return HttpResponseRedirect(reverse_lazy('index'))

    def get_template_names(self):
        if self.request.user.is_superuser:
            return 'list-doctor-record-admin.html'
        else:
            return 'list-doctor-record.html'

    def get_context_data(self, **kwargs):
        context = super(ListDoctorRecord, self).get_context_data(**kwargs)
        context['doctor_record_list'] = \
            DoctorRecord.objects.filter(patient=self.get_object()).order_by('-from_date')
        return context

class StartDoctorRecord(LoginRequiredMixin, generic.FormView):
    """ 管理员创建患者初始就医记录
    """
    form_class = forms.DoctorRecordStartForm

    def get_template_names(self):
        if self.request.user.is_superuser:
            return 'admin-update.html'
        elif self.request.user.is_patient:
            return 'update-user-profile.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('list-doctor-record', kwargs=self.kwargs)
        else:
            return reverse_lazy('patient-list-doctor-record')

    def get_form_kwargs(self):
        kwargs = super(StartDoctorRecord, self).get_form_kwargs()
        if self.request.user.is_superuser:
            kwargs['patient'] = get_object_or_404(Patient, id=self.kwargs['pk'])
        elif self.request.user.is_patient:
            kwargs['patient'] = self.request.user.patient
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(StartDoctorRecord, self).form_valid(form)

class EndDoctorRecord(LoginRequiredMixin, generic.UpdateView):
    """ 管理员控制患者就医结束
    """
    model = DoctorRecord
    form_class = forms.DoctorRecordEndForm

    def get_template_names(self):
        if self.request.user.is_superuser:
            return 'admin-update.html'
        elif self.request.user.is_patient:
            return 'update-user-profile.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('admin-detail-doctor-record', kwargs=self.kwargs)
        else:
            return reverse_lazy('patient-detail-doctor-record', kwargs=self.kwargs)

    def get_object(self, queryset=None):
        if self.request.user.is_patient:
            super_object = super(EndDoctorRecord, self).get_object()
            if super_object.patient != self.request.user.patient:
                return HttpResponseRedirect(reverse_lazy('index'))
        if self.request.user.is_superuser:
            super_object = super(EndDoctorRecord, self).get_object()
        if super_object.end_date:
            return HttpResponseRedirect(reverse_lazy('index'))
        return super_object


class DetailDoctorRecord(generic.DetailView):
    """ 管理员查看患者就医说明
    """
    model = DoctorRecord
    context_object_name = 'record'

    def get_object(self, queryset=None):
        if self.request.user.is_patient:
            if super(DetailDoctorRecord, self).get_object().patient != self.request.user.patient:
                return HttpResponseRedirect(reverse_lazy('index'))
        return super(DetailDoctorRecord, self).get_object()

    def get_template_names(self):
        if self.request.user.is_superuser:
            return 'detail-doctor-record-admin.html'
        else:
            return 'detail-doctor-record.html'


class UpdateDoctorRecord(SuperRequiredMixin, generic.UpdateView):
    """ 管理员查看患者就医说明
    """
    model = DoctorRecord
    template_name = 'admin-update.html'

    def get_success_url(self):
        return reverse('admin-detail-doctor-record', kwargs=self.kwargs)