#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'
import json

from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
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


from .models import Region

def get_region(request, parent_id):

    try:
        if parent_id == '0': parent=None
        else:
            parent=Region.objects.get(id=parent_id)
        c_list = Region.objects.filter(parent=parent)
        ret = [[i.id,i.name] for i in c_list]
    except:
        ret = [[0,'未找到']]

    _data = json.dumps(ret)
    return HttpResponse(content=_data, status=200,
                        content_type='application/json')


@cache_page(60 * 15)
def get_city_js(requests):

    province_list = Region.objects.filter(parent=None)

    ret = [{'n': province.name, 's': [{'n':city.name, 's': [{'n': area.name}
                                                            for area in city.get_children()]}
                                      for city in province.get_children()]}
           for province in province_list]

    _data = json.dumps(ret, ensure_ascii=False)
    return HttpResponse(content=_data, status=200,
                        content_type='application/javascript')