#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms

from .models import Patient

class UpdatePatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ('sex', 'id_no', 'hometown', 'local',
                  'onset_date', 'onset_causes', 'checklist',
                  'disease_quality', 'mood','onset_process')


