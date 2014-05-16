#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
from django.template import loader
from django.core.mail import send_mail
from django.utils.http import int_to_base36
from django.utils.safestring import mark_safe
from django.contrib.sites.models import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import UNUSABLE_PASSWORD, identify_hasher
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from .models import User, Personal, IDENTITY_CHOICES, Unit, Bank
from .mails import send_confirm_email

class BaseRegisterForm(UserCreationForm):
    """ 用户注册表单
    重写了save方法，用于注册后修改身份
    """
    class Meta:
        model = User
        fields=('username', 'identity', 'email')

    class Media:

        js = ('js/register.js',)

    def __init__(self, *args, **kwargs):
        try:
            self.request = kwargs.pop("view_request")
        except (KeyError,AttributeError):
            pass
        super(BaseRegisterForm, self).__init__(*args, **kwargs)

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
        user.identity = int(self.cleaned_data["identity"]) # 修改身份
        if commit:
            user.save()
        return user

class AdminCreateUserForm(BaseRegisterForm):
    """ 用户注册表单
    重写了save方法，用于注册后修改身份
    """
    #identity = forms.ChoiceField(label='注册身份',choices=IDENTITY_CHOICES,
    #                             help_text='请正确选择身份')
    # def save(self, commit=True):
    #     user = super(AdminCreateUserForm, self).save(commit=False)
    #     return user

class RegisterForm(BaseRegisterForm):
    """ 用户注册form
    """
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_mark('email', False)
        send_confirm_email(user.email, self.request.SITE)
        return user




class UpdateUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.fields['is_active'].help_text = '该用户是否允许正常登录'
        self.fields['is_staff'].label = '是否站点管理员'
        self.fields['is_staff'].help_text = ''

    class Meta:
        model = User
        fields=('username','email', 'avatar', 'is_active', 'is_staff',
                'is_superuser', 'spare', 'cellphone', 'spare_phone',
                'qq','score','remark')


class UpdateProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.username
        else:
            return self.cleaned_data['username']

    def clean_email(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.email
        else:
            return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ('username', 'email','last_name', 'first_name',
                  'avatar','spare', 'cellphone', 'spare_phone',
                  'qq',)


class PasswordResetForm(forms.Form):
    error_messages = {
        'unknown': "该邮箱尚未注册！",
        'unusable': "该邮箱尚未激活",
    }
    email = forms.EmailField(label="电子邮件", max_length=254)

    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        UserModel = User
        email = self.cleaned_data["email"]
        self.users_cache = UserModel._default_manager.filter(email__iexact=email)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if not any(user.is_active for user in self.users_cache):
            # none of the filtered users are active
            raise forms.ValidationError(self.error_messages['unknown'])
        if any((user.password == UNUSABLE_PASSWORD)
               for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.pk),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])


class VltFirstFillForm(forms.ModelForm):

    class Meta:
        model = Personal
        exclude = ('user',)

    def __init__(self, user=None,*args, **kwargs):
        super(VltFirstFillForm, self).__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        ret = super(VltFirstFillForm, self).save(commit=False)
        ret.user = self._user
        ret.save()


class VltFillForm(forms.ModelForm):
    class Meta:
        model = Personal
        fields = ('nickname','nationality','belief','height',
                  'weight','marital_status','bear_status','home_phone')



class UnitForm(forms.ModelForm):

    class Meta:
        model = Unit
        exclude = ('user')

    def __init__(self, user=None,*args, **kwargs):
        super(UnitForm, self).__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        ret = super(UnitForm, self).save(commit=False)
        ret.user = self._user
        if commit: ret.save()
        return ret



class BankForm(forms.ModelForm):

    class Meta:
        model = Bank
        exclude = ('user')

    def __init__(self, user=None,*args, **kwargs):
        super(BankForm, self).__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        ret = super(BankForm, self).save(commit=False)
        ret.user = self._user
        ret.save()
