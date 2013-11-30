#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.views import generic
from django.core.urlresolvers import reverse_lazy

from ..utils import SuperUser
from .models import Hospital, Doctor
from .forms import UpdateHospitalForm


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

    model = Hospital
    template_name = 'list-hospital.html'

class DetailHospital(generic.DetailView, SuperUser):

    model = Hospital
    context_object_name = 'hospital'
    template_name = 'detail-hospital.html'

class UpdateHospital(generic.UpdateView, SuperUser):

    model = Hospital
    success_url = reverse_lazy('admin-list-hospital')
    template_name = 'update.html'


class DeleteHospital(generic.DeleteView, SuperUser):

    model = Hospital
    success_url = reverse_lazy('admin-list-hospital')
    template_name = 'confirm_delete.html'


class DetailDoctor(generic.DetailView, SuperUser):

    model = Doctor
    context_object_name = 'doctor'
    template_name = 'detail-doctor.html'

class ListDoctor(generic.ListView, SuperUser):

    model = Doctor
    template_name = 'list-doctor.html'

class UpdateDoctor(generic.UpdateView, SuperUser):

    model = Doctor
    success_url = reverse_lazy('admin-list-doctor')
    template_name = 'update.html'






