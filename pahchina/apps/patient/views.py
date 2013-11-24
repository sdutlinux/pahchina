#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render_to_response as r2r
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm

from .models import Patient
from .forms import UpdatePatientForm
from ..utils import SuperUser

class DetailPatient(generic.DeleteView):

    model = Patient
    context_object_name = 'patient'
    template_name = 'detail-patient.html'

class ListPatient(generic.ListView, SuperUser):

    model = Patient
    context_object_name = 'patient_list'
    template_name = 'list-patient.html'

class UpdatePatient(generic.UpdateView, SuperUser):

    model = Patient
    form_class = UpdatePatientForm
    success_url = reverse_lazy('list-patient')
    template_name = 'update-patient.html'

class Profile(generic.TemplateView):

    template_name = 'profile-patient.html'