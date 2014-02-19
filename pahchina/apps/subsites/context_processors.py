#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Site

def site(request):
    """
    模板中的`SITE`全局变量
    """
    domain=request.get_host().split(":")[0]

    try:
        current_site = Site.objects.get(domain=domain)
    except Site.DoesNotExist:
        current_site = Site.objects.get(id=1)

    return {'SITE': current_site}
