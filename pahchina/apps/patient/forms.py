#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
#from django.contrib.localflavor.cn.forms import CNProvinceSelect

from .models import Patient, Dosage
from ..utils.fields import ChoiceWithOtherWidget, ChoiceWithOtherField


class UpdatePatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        exclude = ('user',)


class CreateDosageForm(forms.ModelForm):
    """ 用于患者创建自己的用药状况
    """

    class Meta:
        model = Dosage
        fields = ('drug', 'dose')

    def __init__(self, patient=None, *args, **kwargs):
        super(CreateDosageForm, self).__init__(*args, **kwargs)
        self._patient = patient

    def save(self, commit=True):
        context = super(CreateDosageForm, self).save(commit=False)
        context.patient = self._patient
        context.save()


class AdminCreateDosageForm(forms.ModelForm):
    """ 管理员用来创建患者的用药状况
    """

    class Meta:
        model = Dosage
        fields = ('drug', 'dose')

    def save(self, commit=True):
        super(AdminCreateDosageForm, self).save()