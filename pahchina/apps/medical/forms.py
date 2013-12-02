#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms

from .models import Hospital, Doctor, Record

class UpdateHospitalForm(forms.ModelForm):
    """ 医院用来更新自己的信息
    """

    class Meta:
        model = Hospital
        fields = ('local', 'is_community', 'level')


class RecordForm(forms.ModelForm):

    class Meta:
        model = Record
        exclude = ('patient')


    def __init__(self, patient=None,*args,**kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self._patient = patient

    def save(self, commit=True):
        context = super(RecordForm, self).save(commit=False)
        context.patient = self._patient
        context.save()