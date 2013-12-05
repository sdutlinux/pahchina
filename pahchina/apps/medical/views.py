#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import Http404

from ..utils import SuperUser, SuperRequiredMixin
from ..patient.models import Patient

from .models import Hospital, Doctor, Record, DoctorRecord
from .forms import UpdateHospitalForm, RecordForm, \
    DoctorRecordStartForm, DoctorRecordEndForm


class UpdateHospitalProfile(generic.UpdateView):
    """ 更新医院信息，管理员和医院通用
    """
    model = Hospital
    form_class = UpdateHospitalForm

    def get_object(self, queryset=None):
        if self.request.user.is_superuser:
            self.success_url = reverse_lazy('profile-hospital')
            self.template_name = 'update.html'
            self.object = super(UpdateHospitalProfile, self).get_object()
        elif self.request.user.is_hospital:
            self.success_url = reverse_lazy('admin-list-hospital')
            self.template_name = 'update-user-profile.html'
            self.object = self.request.user.hospital
        return self.object

class ListHospital(SuperRequiredMixin, generic.ListView):
    """ 列出所有医院
    """
    model = Hospital
    template_name = 'list-hospital.html'

class DetailHospital(SuperRequiredMixin, generic.DetailView):
    """ 管理员查看医院详细信息
    """
    model = Hospital
    context_object_name = 'hospital'
    template_name = 'detail-hospital.html'




#class DeleteHospital(SuperRequiredMixin, generic.DeleteView):
#    """ 管理员删除医院
#    """
#    model = Hospital
#    success_url = reverse_lazy('admin-list-hospital')
#    template_name = 'confirm_delete.html'


class DetailDoctor(SuperRequiredMixin, generic.DetailView):
    """ 医生查看医生详情
    """
    model = Doctor
    context_object_name = 'doctor'
    template_name = 'detail-doctor.html'

class ListDoctor(SuperRequiredMixin, generic.ListView):
    """ 管理员列出所有医生
    """
    model = Doctor
    template_name = 'list-doctor.html'

class UpdateDoctor(SuperRequiredMixin, generic.UpdateView):
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

class ListDoctorRecord(generic.DetailView):
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
            raise Http404

    def get_template_names(self):
        if self.request.user.is_superuser:
            return 'list-doctor-record-admin.html'
        else:
            return 'list-doctor-record.html'

    def get_context_data(self, **kwargs):
        context = super(ListDoctorRecord, self).get_context_data(**kwargs)
        context['doctor_record_list'] = \
            DoctorRecord.objects.filter(patient=self.get_object())
        return context

class StartDoctorRecord(generic.FormView):
    """ 管理员创建患者初始就医记录
    """
    form_class = DoctorRecordStartForm

    def get_template_names(self):
        if self.request.user.is_superuser:
            return 'update.html'
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

class EndDoctorRecord(generic.UpdateView):
    """ 管理员控制患者就医结束
    """
    model = DoctorRecord
    form_class = DoctorRecordEndForm

    def get_template_names(self):
        if self.request.user.is_superuser:
            return 'update.html'
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
            if super_object.patient == self.request.user.patient:
                return super_object
        if self.request.user.is_superuser:
            return super(EndDoctorRecord, self).get_object()


class DetailDoctorRecord(generic.DetailView):
    """ 管理员查看患者就医说明
    """
    model = DoctorRecord
    context_object_name = 'record'

    def get_object(self, queryset=None):
        if self.request.user.is_patient:
            if super(DetailDoctorRecord, self).get_object().patient != self.request.user.patient:
                raise Http404
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
    template_name = 'update.html'

    def get_success_url(self):
        return reverse('admin-detail-doctor-record', kwargs=self.kwargs)