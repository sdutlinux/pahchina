#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
from django.forms.models import model_to_dict, fields_for_model
from django.contrib.sites.models import Site

from .models import Site
from ..accounts.models import User


class StaffSiteForm(forms.ModelForm):

    """ 分站管理员使用
    """

    class Meta:
        model = Site
        exclude = ('admin')