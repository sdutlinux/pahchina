#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django import forms
from .models import Donate, Itemized

class BaseDonateForm(forms.ModelForm):
    """ 捐赠Form基类
    需要添加 Meta(BaseDonateForm.Meta): 中的 fields or excludes
    就像下面的 AdminDonateForm and UserDonateForm
    """
    class Meta:
        model = Donate

    def __init__(self, user=None, target_user=None, *args, **kwargs):
        super(BaseDonateForm, self).__init__(*args, **kwargs)
        self._user = user
        self._target_user = target_user

    def save(self, commit=False):
        donate = super(BaseDonateForm, self).save(commit=False)
        if self._user:
            donate.user = self._user
            donate.save()
        if self._target_user:
            donate.target_user = self._target_user
            donate.save()
        super(BaseDonateForm, self).save(commit=True)

class AdminDonateForm(BaseDonateForm):
    """ 管理员创建捐赠条目
    """
    username = forms.CharField(label='捐赠者',)

    class Meta(BaseDonateForm.Meta):
        #model = Donate
        exclude = ('number','user', 'target_user', 'is_true','mark_true_date',)


class UserDonateForm(BaseDonateForm):
    """ 用户捐赠
    """
    class Meta(BaseDonateForm.Meta):
        exclude = ('number','user','is_true','mark_true_date', 'residue', 'target_user')





class ItemizedForm(forms.ModelForm):

    class Meta:
        model = Itemized
        exclude = ('donate', 'created_user')

    def __init__(self, donate=None, user=None, *args, **kwargs):
        super(ItemizedForm, self).__init__(*args, **kwargs)
        self._donate = donate
        self._user = user

    def clean_cast(self):
        cast = self.cleaned_data['cast']
        if self._donate.residue -  cast< 0:
            raise forms.ValidationError('填写错误，余额将小于零！')
        else:
            return cast

    def save(self, commit=True):
        #itemized, created = Itemized.objects.get_or_create(id=self.instance.id)
        #print itemized, created
        form_data = super(ItemizedForm, self).save(commit=False)

        if form_data.id:
            # 后来修改时，同步修改donate余额
            itemized_instance = Itemized.objects.get(id=form_data.id)
            self._donate.residue += (itemized_instance.cast - self.cleaned_data['cast'])
            super(ItemizedForm, self).save()
        else:
            form_data.donate = self._donate
            form_data.created_user = self._user
            form_data.save()
            self._donate.residue -= self.cleaned_data['cast']
        self._donate.save()