#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'


from django.contrib import admin
from .models import Donate

class DonateAdmin(admin.ModelAdmin):
    list_display = ('number', 'money','create_time')



admin.site.register(Donate, DonateAdmin)