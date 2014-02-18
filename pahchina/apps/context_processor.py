#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.contrib.sites.models import Site

def site(request):

    return {
        'site': Site.objects.get_current()
    }