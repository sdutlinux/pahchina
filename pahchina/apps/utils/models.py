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


    def instance_dict(instance, key_format=None):
        "Returns a dictionary containing field names and values for the given instance"
        from django.db.models.fields.related import ForeignKey
        if key_format:
            assert '%s' in key_format, 'key_format must contain a %s'
        key = lambda key: key_format and key_format % key or key

        d = {}
        for field in instance._meta.fields:
            attr = field.name
            value = getattr(instance, attr)
            if value is not None and isinstance(field, ForeignKey):
                value = value._get_pk_val()
            d[key(attr)] = value
        for field in instance._meta.many_to_many:
            d[key(field.name)] = [obj._get_pk_val() for obj in getattr(instance, field.attname).all()]
        return d