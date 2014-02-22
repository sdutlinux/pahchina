#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
#from django.contrib.localflavor.cn.forms import CNProvinceSelect

from .models import Patient, Dosage
from ..utils.fields import ChoiceWithOtherWidget, ChoiceWithOtherField



class UpdatePatientForm(forms.ModelForm):

    #init_diag_hosp_type = ChoiceWithOtherField(choices=[
    #                                           ("sjyy","省级医院"),
    #                                           ("xsjyy","县市级医院"),
    #                                           ("sqyy","社区医院"),
    #                                           ("xzyy","乡镇医院"),
    #                                           ("ncyy","农村医院"),
    #                                           ("srzs","私人诊所"),
    #                                           ('other',""),])
    #age = ChoiceWithOtherField(choices=[
    #     (0, '15-29'),
    #     (1, '30-44'),
    #     (2, '45-60'),
    #     (3, 'Other, please specify:')
    # ])


    class Meta:
        model = Patient
        exclude = ('user',)

        widgets = {
            #'init_diag_hosp_type': ChoiceWithOtherField(choices=(
            #                                   ("sjyy","省级医院"),
            #                                   ("xsjyy","县市级医院"),
            #                                   ("sqyy","社区医院"),
            #                                   ("xzyy","乡镇医院"),
            #                                   ("ncyy","农村医院"),
            #                                   ("srzs","私人诊所"),
            #                                   ("other","其他（请注明）"),
            #                               ),),
        }


class CreateDosageForm(forms.ModelForm):
    """ 用于患者创建自己的用药状况
    """
    class Meta:
        model = Dosage
        fields = ('drug', 'dose')

    def __init__(self, patient=None,*args,**kwargs):
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