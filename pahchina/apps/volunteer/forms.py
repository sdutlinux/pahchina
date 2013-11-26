#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from .models import Volunteer
from django.forms import ModelForm

class VolunteerForm(ModelForm):

    class Meta:
        model = Volunteer
        exclude = ('liveness',)
