#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django.contrib import admin
from .models import Sorts, News

class SortsAdmin(admin.ModelAdmin):
    list_display = ('name','parent')

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title','author','sort')

admin.site.register(News, NewsAdmin)
admin.site.register(Sorts, SortsAdmin)