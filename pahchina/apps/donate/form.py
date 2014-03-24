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

    def clean_cast(self):
        cast = self.cleaned_data['cast']
        if self._donate.residue -  cast< 0:
            raise forms.ValidationError('填写错误，余额将小于零！')
        else:
            return cast

    def save(self, commit=True):
        #itemized, created = Itemized.objects.get_or_create(id=self.instance.id)
        #print itemized, created
        form_data = super(ItemizedForm, self).save(commit=False)

        if form_data.id:
            # 后来修改时，同步修改donate余额
            itemized_instance = Itemized.objects.get(id=form_data.id)
            self._donate.residue += (itemized_instance.cast - self.cleaned_data['cast'])
            super(ItemizedForm, self).save()
        else:
            form_data.donate = self._donate
            form_data.created_user = self._user
            form_data.save()
            self._donate.residue -= self.cleaned_data['cast']
        self._donate.save()


        # class ItemizedUpdateForm(forms.ModelForm):
        #
        #     class Meta:
        #         model = Itemized
        #         exclude = ('number')