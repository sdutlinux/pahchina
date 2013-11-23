#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.Form):

    email=forms.EmailField(label=_(u"邮箱 "),max_length=30,
                           widget=forms.TextInput(attrs={'size': 30,}),
                           help_text="")
    username=forms.CharField(label=_(u"用户名 "),max_length=30,
                             widget=forms.TextInput(attrs={'size': 20,}),
                           help_text="")
    password1=forms.CharField(label=_(u"密码 "),max_length=30,
                             widget=forms.PasswordInput(attrs={'size': 20,}),
                           help_text="")
    password2=forms.CharField(label=_(u"重复密码 "),max_length=30,
                                widget=forms.PasswordInput(attrs={'size': 20,}),
                           help_text="")

    def clean_password(self):

        if self.password1 != self.password2:
            raise forms.ValidationError("两次输入的密码不相同")