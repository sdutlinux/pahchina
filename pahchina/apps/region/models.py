#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.db import models
from django.utils.html import mark_safe

from mptt.models import MPTTModel

class Region(MPTTModel):
    """ 用于标注省市县三级联动
    """

    name = models.CharField(verbose_name='名称', max_length=30)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name='地区'