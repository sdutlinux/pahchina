#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf import settings
from django.shortcuts import get_object_or_404

from ..news.models import Sorts


def index(request):
    """ 首页菜单栏
    """
    sort_list = Sorts.objects.filter(is_navbar=True).order_by('-weight')

    return {'sort_list': sort_list}

