#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

from ..accounts.models import User
from ..patient.models import SEX_CHOICES, Patient


class Hospital(models.Model):

    user = models.OneToOneField(User, verbose_name='医院名称')
    local = models.CharField(verbose_name='所在地区', max_length=20)
    is_community = models.BooleanField(verbose_name='是否治疗中心')
    level = models.CharField(verbose_name='医院等级', max_length=20)

    def model_name(self):
        return "医院"

    def __unicode__(self):
        return self.user.username


class Doctor(models.Model):

    user = models.OneToOneField(User, verbose_name='医生姓名')
    hospital = models.ForeignKey(Hospital, verbose_name='所在医院', blank=True, null=True)

    sex = models.CharField(verbose_name='性别', default='2', choices=SEX_CHOICES, max_length=1)
    age = models.CharField(verbose_name='年龄', max_length=2, blank=True, null=True)

    job_title = models.CharField(verbose_name='职称', max_length=10, blank=True, null=True)

    def get_sex(self):
        if self.sex == '1': return '男'
        elif self.sex == '0': return '女'
        else: return '隐私'

    def model_name(self):

        return '医生'

    def __unicode__(self):
        return self.user.username
