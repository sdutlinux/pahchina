#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from tinymce import models as tiny_models
from ckeditor.fields import RichTextField

from ...apps.utils.models import TimeStampedModel
from ...apps.accounts.models import User
from ...apps.website.models import Website

# Create your models here.
class Sorts(MPTTModel):
    name = models.CharField(max_length=20, verbose_name="分类名称", unique=True)
    description = models.TextField(verbose_name='描述', max_length=500)
    parent = TreeForeignKey("self", verbose_name='所属分类', blank=True, null=True,
                            related_name="children",
                            help_text='空则为顶级分类')

    is_navbar = models.BooleanField(verbose_name='是否标题栏显示', help_text='反选为否')
    is_index = models.BooleanField(verbose_name='是否首页显示', help_text='是否在首页内容区显示')
    weight = models.IntegerField(verbose_name='分类权重', blank=True, null=True,
                                 help_text='分类显示顺序，请输入整数, 整数越大，位置越靠前')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta(MPTTModel.Meta):
        verbose_name = '分类'

    def __unicode__(self):
        return self.name


class News(TimeStampedModel):

    title = models.CharField(max_length=50, verbose_name='标题', unique=True)
    content = RichTextField(verbose_name='内容', config_name="default")

    author = models.ForeignKey(User, verbose_name='作者')

    published_date = models.DateField(verbose_name='发布时间', help_text='用于显示新闻的发布时间。')
    site = models.ManyToManyField(Website, verbose_name='所属站点')

    is_index = models.BooleanField(verbose_name='首页显示', default=False)
    is_draft = models.BooleanField(verbose_name='草稿', default=False)
    is_push = models.BooleanField(verbose_name='推送', default=False)
    is_top = models.BooleanField(verbose_name='置顶', default=False)

    img = models.ImageField(upload_to='news/show', verbose_name='推广图片', blank=True, null=True)
    sort = models.ForeignKey(Sorts, verbose_name='分类')

    class Meta:
        verbose_name = '新闻'

    def __unicode__(self):
        return self.title

    def get_draft(self):
        return '草稿' if self.is_draft else '非草稿'

    def get_push(self):
        return '推送' if self.is_push else '不推送'

    def get_top(self):
        return '置顶' if self.is_top else '非置顶'





