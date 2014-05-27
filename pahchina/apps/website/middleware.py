#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

import logging

from django.conf import settings
from django.utils.cache import patch_vary_headers

from .models import Website as Site

class SubSiteMiddleWare:
    """
    """
    def process_request(self, request):
        host = request.META["HTTP_HOST"].split(":")[0]
        try:
            request.SITE = Site.objects.get(domain=host)
        except Site.DoesNotExist:
            request.SITE = Site.objects.get(id=1)

    def process_response(self, request, response):

        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))

        return response


