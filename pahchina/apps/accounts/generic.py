#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render_to_response as r2r, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import Permission, PermissionManager, PermissionsMixin
#from django.


from ..utils import  SuperRequiredMixin
from ..patient.models import Patient
from ..medical.models import Doctor, Hospital
from ..volunteer.models import Volunteer


#class Update(SuperRequiredMixin, generic.UpdateView):

