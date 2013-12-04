#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
from django.utils import timezone
from django.http import Http404
from django.contrib.admin import widgets

#from datetimewidget.widgets import DateTimeWidget

from .models import Hospital, Doctor, Record, DoctorRecord

class UpdateHospitalForm(forms.ModelForm):
    """ 医院用来更新自己的信息
    """

    class Meta:
        model = Hospital
        fields = ('local', 'is_community', 'level')


class RecordForm(forms.ModelForm):

    class Meta:
        model = Record
        fields = ('content',)


    def __init__(self, patient=None,*args,**kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self._patient = patient

    def save(self, commit=True):
        context = super(RecordForm, self).save(commit=False)
        context.patient = self._patient
        context.save()

class DoctorRecordStartForm(forms.ModelForm):

    class Meta:
        model = DoctorRecord
        fields = ('doctor','from_description',)

    def __init__(self, patient=None, *args, **kwargs):
        super(DoctorRecordStartForm, self).__init__(*args, **kwargs)
        self._patient = patient

    def clean_doctor(self):
        doctor = self.cleaned_data["doctor"]
        try:
            last_one = DoctorRecord.objects.filter(patient=self._patient).order_by('-id')[0]
            if doctor == last_one.doctor and last_one.end_date is None:
                raise forms.ValidationError('正在接受该医生的治疗！')
        except IndexError,DoctorRecord.DoesNotExist:
            return doctor
        return doctor


    def save(self, commit=True):
        context = super(DoctorRecordStartForm, self).save(commit=False)
        context.patient = self._patient
        context.save()

class DoctorRecordEndForm(forms.ModelForm):

    class Meta:
        model = DoctorRecord
        fields = ('end_description',)

    def save(self, commit=True):
        context = super(DoctorRecordEndForm, self).save(commit=False)
        context.end_date = timezone.now()
        context.save()

#dateTimeOptions = {
    #'format': 'dd/mm/yyyy HH:ii P',
    #'format': 'yyyy-mm-dd HH:ii:ss',
    #'autoclose': 'true',
    #'showMeridian' : 'true'
#}

#class DoctorRecordForm(forms.ModelForm):
#
#    #def __init__(self, *args, **kwargs):
#    #    super(DoctorRecordForm, self).__init__(*args, **kwargs)
#    #    self.fields['from_date'].widget
#
#    class Meta:
#        model = DoctorRecord
#        widgets = {
#            'from_date': DateTimeWidget(options = dateTimeOptions),
#            'end_date': DateTimeWidget(options = dateTimeOptions),
#        }