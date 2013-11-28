#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'
from django import forms
from .models import Activity

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        exclude = ('volunteer',)

#class VolunteerChoose(forms.ModelForm):
#    volunteer = forms.ModelMultipleChoiceField()
#    class Meta:
#        model = Activity
#        field = ('Volunteer',)