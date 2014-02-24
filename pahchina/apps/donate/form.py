#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django import forms
from .models import Donate, Itemized


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

class ItemizedForm(forms.ModelForm):

    class Meta:
        model = Itemized
        exclude = ('residue','number')

    def __init__(self, donate=None, *args, **kwargs):
        super(ItemizedForm, self).__init__(*args, **kwargs)
        self._number = donate

    def save(self, commit=True):
        if self._number:
            itemized = super(ItemizedForm, self).save(commit=False)
            itemized.number = self._number
            itemized.save()
        else:
            super(ItemizedForm, self).save(commit=True)

    def clean_residue(self):
        temp = Itemized.objects.filter(number=self.number).order_by('-time')
        residue = temp[0].residue - self.cast
        if residue < 0 :
            raise forms.ValidationError('填写错误，余额将小于零！')