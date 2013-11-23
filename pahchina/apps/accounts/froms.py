#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User

IDENTITY_CHOICES = (
    ('5,','志愿者'),
    ('1,', '患者'),
    ('2,','医生'),
    ('3,','医院'),
    ('4,','捐献者'),
    ('6,','药商'),
)

class RegisterForm(UserCreationForm):
    """ 用户注册表单
    choices = (
        ('1,', '患者'),
        ('2,','医生'),
        ('3,','医院'),
        ('4,','捐献者'),
        ('5,','志愿者'),
        ('6,','药商'),
    )
    """
    identity = forms.ChoiceField(label='注册身份',choices=IDENTITY_CHOICES,
                                 help_text='请正确选择身份')

    class Meta:
        model = User
        fields=('username',)

    def clear_identity(self):
        identity = self.cleaned_data.get("identity")
        for i in identity:
            if i not in '123456,':
                raise forms.ValidationError('身份不合法！')