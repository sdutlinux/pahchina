#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.conf import settings
from django.shortcuts import get_object_or_404

from ..news.models import Sorts, News


def index(request):
    """ 首页菜单栏
    """
    sort_list = Sorts.objects.filter(is_navbar=True).order_by('-weight')
    news_list = News.objects.all().order_by('-published_date')[:11]

    return {
        'sort_list': sort_list,
        'news_list': news_list,
    }

