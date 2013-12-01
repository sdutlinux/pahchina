#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'


from django.contrib import admin
from .models import Donate
from .models import Itemized

class DonateAdmin(admin.ModelAdmin):
    list_display = ('number', 'money','create_time')

class ItemizedAdmin(admin.ModelAdmin):
    list_display = ('number', 'time','cast','residue')

admin.site.register(Donate, DonateAdmin)
admin.site.register(Itemized, ItemizedAdmin)





