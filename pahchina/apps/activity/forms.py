#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'
from django.forms import ModelForm
from .models import Activity

class ActivityForm(ModelForm):
    class Meta:
        model = Activity
        exclude = ('volunteer',)
