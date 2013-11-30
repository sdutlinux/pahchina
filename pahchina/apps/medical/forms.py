#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms

from .models import Hospital, Doctor

class UpdateHospitalForm(forms.ModelForm):
    """ 医院用来更新自己的信息
    """

    class Meta:
        model = Hospital
        fields = ('local', 'is_community', 'level')