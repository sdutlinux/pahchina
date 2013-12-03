#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.db import models

class TimeStampedModel(models.Model):

    """工具类
    用来给你的model添加下面两个字段，分别是创建时间和更新时间
    Usage: class YourModel(TimeStampedModel): ...
    """

    created_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        abstract = True