#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.db import models

from ..accounts.models import User

class TimeStampedModel(models.Model):

    """工具类
    用来给你的model添加下面两个字段，分别是创建时间和更新时间
    Usage: class YourModel(TimeStampedModel): ...
    """

    created_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    updated_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        abstract = True



class OperateHistory(models.Model):

    """ 操作历史
    记录： Date, user, operate(<create><update><delete>), target, information.
    备忘： 通过方法 创建历史 与 查询历史
    """

    created_date = models.DateTimeField(verbose_name='日期', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='操作人')
    operate = models.CharField(verbose_name='操作内容', max_length=10)
    target = models.CharField(verbose_name='目标内容', max_length=10)
    info = models.TextField(verbose_name='详细内容', max_length=100, help_text='操作的详细内容')

    def __unicode__(self):
        return "%s-%s at %s"%(self.user, self.operate, self.created_date)

    class Meta:
        verbose_name = '操作历史'