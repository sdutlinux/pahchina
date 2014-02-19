#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'paomian'

from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title','content','is_draft','is_push','is_top','img','sort')

    def __init__(self, author=None, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self._user = author

    def save(self, commit=False):
            news = super(NewsForm, self).save(commit=False)
            news.author = self._user
            news.save()
