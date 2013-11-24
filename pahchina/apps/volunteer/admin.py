#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'
from django.contrib import admin
from .models import Volunteer

class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user','sex','phone')

admin.site.register(Volunteer, VolunteerAdmin)