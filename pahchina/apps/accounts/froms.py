#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

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

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('该用户名已被注册！')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('两次输入的密码不相同！')
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.identity=self.cleaned_data["identity"] # 修改身份
        if commit:
            user.save()
        return user

class UpdateUserForm(forms.ModelForm):



    class Meta:
        model = User
        fields=('username', 'email', 'avatar', 'is_active')