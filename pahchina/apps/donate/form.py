#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django import forms
from .models import Donate, Itemized


class DonateFormUser(forms.ModelForm):

    class Meta:
        model = Donate
        exclude = ('number','user','is_true','mark_true_date', 'residue')

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
        exclude = ('donate', 'created_user')

    def __init__(self, donate=None, user=None, *args, **kwargs):
        super(ItemizedForm, self).__init__(*args, **kwargs)
        self._donate = donate
        self._user = user

    def clean_residue(self):
        if self._donate.residue - self.cast < 0:
            raise forms.ValidationError('填写错误，余额将小于零！')

    def save(self, commit=True):
        if self.instance.id:
            # 后来修改时，同步修改donate余额
            self._donate.residue += (self.instance.cast - self.cleaned_data['cast'])
            super(ItemizedForm, self).save(commit=True)
        else:
            itemized = super(ItemizedForm, self).save(commit=False)
            itemized.donate = self._donate
            itemized.created_user = self._user
            itemized.save()
            self._donate.residue -= self.cleaned_data['cast']
        self._donate.save()


# class ItemizedUpdateForm(forms.ModelForm):
#
#     class Meta:
#         model = Itemized
#         exclude = ('number')