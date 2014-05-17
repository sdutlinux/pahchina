#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.db import models
from django.utils.html import mark_safe

from mptt.models import MPTTModel

from ..accounts.models import User
from ..utils.models import TimeStampedModel
from ..website.models import Website

class Region(MPTTModel):
    """ 用于标注省市县三级联动
    """

    name = models.CharField(verbose_name='名称', max_length=30)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")

    website = models.ForeignKey(Website, verbose_name='所属网站', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name='地区'



class LivingRegion(TimeStampedModel):
    """ 用户的居住信息
    """
    user = models.ForeignKey(User)

    province = models.CharField(verbose_name='省份', max_length=30,)
    city = models.CharField(verbose_name='城市', max_length=30, blank=True, null=True)
    area = models.CharField(verbose_name='地区', max_length=30, blank=True, null=True)

    cate = models.CharField(verbose_name='居住类型', help_text="选择所在的省市县",
                            max_length= 10, choices=(('apartment', '户籍所在地'),('household', '常住地'),))

    class Meta:
        verbose_name = '居住信息'

    def __unicode__(self):
        return self.province + self.city +'市'+ self.area

    def get_location(self):
        """ 获取全部信息
        ret: 山东省淄博市张店区
        """
        return self.province + self.city + self.area

    def clean_cate(self):
        pass

def set_user_region(user, cate, province, city, area):
    """ 设置用户住址
    """
    try:
        _region = LivingRegion.objects.get(user=user, cate=cate)
    except LivingRegion.DoesNotExist:
        _region =LivingRegion(user=user, cate=cate)
    _region.province, _region.city, _region.area = province, city, area
    _region.save()
    return _region