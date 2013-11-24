#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django.contrib import admin
from .models import Activity

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time', 'activity_time')



admin.site.register(Activity, ActivityAdmin)