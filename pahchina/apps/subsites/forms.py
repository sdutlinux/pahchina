#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django import forms
from django.forms.models import model_to_dict, fields_for_model
from django.contrib.sites.models import Site

from .models import Site
from ..accounts.models import User


#class SiteForm(forms.ModelForm):
#
#    def __init__(self, instance=None, *args, **kwargs):
#        _fields = ('name', 'domain',)
#        _initial = kwargs.pop('initial')
#        _initial = model_to_dict(instance.site, _fields) if instance is not None else {}
#        super(SiteForm, self).__init__(initial=_initial, instance=instance, *args, **kwargs)
#        self.fields.update(fields_for_model(Site, _fields))
#        #self.fields['admin'].choices=[(u.id,u.username) for u in User.objects.filter(is_staff=True)]
#
#
#    class Meta:
#        model = SiteProfile
#        exclude = ('site',)
#
#    def clear_domain(self):
#        domain = self.cleaned_data.get("domain")
#        if Site.objects.filter(doamin=domain).count() != 0:
#            raise forms.ValidationError('该域名已被占用')
#
#
#    def save(self, *args, **kwargs):
#         s = self.instance.site
#         s.name = self.cleaned_data['name']
#         s.domain=self.cleaned_data['domain']
#         s.save()
#         profile = super(SiteForm, self).save(*args, **kwargs)
#         return profile
