#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
from django.forms.models import model_to_dict, fields_for_model
from django.contrib.sites.models import Site
from django.db.models import Q

from .models import Website, Links
from ..accounts.models import User
from ..region.models import Region

class StaffSiteForm(forms.ModelForm):

    """ 分站管理员使用
    """

    class Meta:
        model = Website
        exclude = ('admin')

class CreateSiteForm(forms.ModelForm):
    """ 管理员创建站点
    """

    def __init__(self, *args, **kwargs):
        super(CreateSiteForm, self).__init__(*args, **kwargs)
        self.fields['admin'].queryset = User.objects.filter(is_staff=True,
                                                            is_superuser=False,
                                                            website=None)
    class Meta:
        model = Website

class RegionWebsiteForm(forms.ModelForm):

    regions = forms.ModelMultipleChoiceField(label='城市列表',queryset=None,
                                             help_text='按住<b>Ctrl</b>键多选')

    def __init__(self, *args, **kwargs):
        super(RegionWebsiteForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['regions'].queryset=Region.objects.filter(Q(parent=None, website=self.instance) | Q(parent=None, website=None))
        self.fields['regions'].initial = self.instance.region_set.all()

    def save(self, commit=True):
        ret = super(RegionWebsiteForm, self).save(commit=False)
        old_region_list = set(Region.objects.filter(website=self.instance))
        new_region_list = set(self.cleaned_data['regions'])
        for r in old_region_list-new_region_list:
            r.website = None
            r.save()
        for r in new_region_list - old_region_list:
            r.website = self.instance
            r.save()
        ret.save()

    class Meta:
        model = Website
        fields = ('name',)

class MyFreLinkForm(forms.ModelForm):
    """ 友情链接Form
    """
    def __init__(self, user=None,*args, **kwargs):
        super(MyFreLinkForm, self).__init__(*args, **kwargs)
        self._user = user

    def save(self, commit=True):
        ret = super(MyFreLinkForm, self).save(commit=False)
        ret.site = self._user.website
        ret.save()

    class Meta:
        model = Links
        fields = ('name', 'url')