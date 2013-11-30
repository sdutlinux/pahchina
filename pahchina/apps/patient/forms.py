#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
#from django.contrib.localflavor.cn.forms import CNProvinceSelect

from .models import Patient, Dosage

class UpdatePatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ('sex', 'id_no', 'hometown', 'local',
                  'onset_date', 'onset_causes', 'checklist',
                  'disease_quality', 'mood','onset_process')


class CreateDosageForm(forms.ModelForm):

    class Meta:
        model = Dosage
        fields = ('drug', 'dose')

    def __init__(self, user=None,*args,**kwargs):
        super(CreateDosageForm, self).__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        context = super(CreateDosageForm, self).save(commit=False)
        context.patient = self._user.patient
        context.save()