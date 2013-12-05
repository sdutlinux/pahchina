#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from ...apps.utils.models import TimeStampedModel
from ...apps.accounts.models import User

# Create your models here.
class Sorts(MPTTModel):
    name=models.CharField(max_length=20,verbose_name="分类名称",unique=True)
    parent=TreeForeignKey("self", blank=True, null=True, related_name="children")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return self.name


class News(TimeStampedModel):
    title = models.CharField(max_length=50, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.ForeignKey(User, verbose_name='作者')
    #site = models.ManyToManyField()
    is_draft = models.BooleanField(verbose_name='草稿')
    is_push = models.BooleanField(verbose_name='推送')
    is_top = models.BooleanField(verbose_name='置顶')
    img = models.ImageField(upload_to='news/show', verbose_name='推广图片')
    sort = models.ForeignKey(Sorts, verbose_name='分类')

    def get_draft(self):
        if self.is_draft:
            return '草稿'
        else:
            return '非草稿'

    def get_push(self):
        if self.is_push:
            return '推送'
        else:
            return '不推送'

    def get_top(self):
        if self.is_top:
            return '置顶'
        else:
            return '非置顶'





