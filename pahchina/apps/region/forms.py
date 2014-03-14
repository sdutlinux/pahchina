#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from .models import LivingRegion

class UserUpdateRegionForm(forms.ModelForm):
    """ 用户更新个人居住信息
    """
    
    class Meta:
        model = LivingRegion
        fields = ('province', 'city', 'area')

    class Media:

        js = ('js/jquery.cxselect.min.js',)

    def __init__(self, user=None, cate=None, *args, **kwargs):
        super(UserUpdateRegionForm, self).__init__(*args, **kwargs)
        self._user = user
        self._cate = cate # 地址信息类型， 户籍地还是居住地

    def save(self, commit=True):
        try:
            _region = LivingRegion.objects.get(user=self._user, cate=self._cate)
        except LivingRegion.DoesNotExist:
            _region =LivingRegion(user=self._user, cate=self._cate)
        _region.province = self.cleaned_data['province']
        _region.city = self.cleaned_data['city']
        _region.area = self.cleaned_data['area']
        _region.save()