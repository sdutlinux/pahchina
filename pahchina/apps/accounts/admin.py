#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name')


admin.site.register(User, UserAdmin)
