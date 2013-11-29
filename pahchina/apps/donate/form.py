#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django import forms
from .models import Donate


#class DonateForm(forms.ModelForm):
#    class Meta:
#        model = Donate
#        fields =

class DonateFormUser(forms.ModelForm):

    class Meta:
        model = Donate
        exclude = ('number','user','istrue','true_time')

    def __init__(self, user=None, *args, **kwargs):
        super(DonateFormUser, self).__init__(*args, **kwargs)
        self._user = user
        
    def save(self, commit=False):
        if  self._user:
            donate = super(DonateFormUser, self).save(commit=False)
            donate.user = self._user
            donate.save()
        else:
            super(DonateFormUser, self).save(commit=True)