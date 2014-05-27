#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

import json

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render_to_response as r2r, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import Permission, PermissionManager, PermissionsMixin
from django.contrib.sites.models import Site, SiteManager
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from .models import User

def check_username(request, username):

    try:
        User.objects.get(username=username)
        ret = {"status": False}
    except User.DoesNotExist:
        ret = {"status": True}

    _data = json.dumps(ret)
    return HttpResponse(content=_data, status=200, content_type='application/json')

@csrf_exempt
def check_email(request):

    if request.method != "POST": raise Http404
    try:
        email = request.POST['email']
        User.objects.get(email=email)
        ret = {"status": False}
    except KeyError:
        raise Http404
    except User.DoesNotExist:
        ret = {"status": True}

    _data = json.dumps(ret)
    return HttpResponse(content=_data, status=200, content_type='application/json')