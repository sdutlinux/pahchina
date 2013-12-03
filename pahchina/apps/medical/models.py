#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

from ..utils.models import TimeStampedModel
from ..utils.choices import DOCTOR_CHOICES, get_full_desc
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

    job_title = models.CharField(verbose_name='职称', max_length=10, blank=True, null=True,
                                 choices=DOCTOR_CHOICES)

    def get_sex(self):
        if self.sex == '1': return '男'
        elif self.sex == '0': return '女'
        else: return '隐私'

    def get_job_title(self):
        """ 获取医生职称
        """
        return get_full_desc(self.job_title, choices=DOCTOR_CHOICES)

    def model_name(self):

        return '医生'

    def __unicode__(self):
        return self.user.username


class Record(TimeStampedModel):
    """ 患者的病例
    More: 此处可用 **unique_for_？？** 来限制病例的创建频率
    """
    patient = models.ForeignKey(Patient, verbose_name='患者', blank=True)
    content = models.TextField(verbose_name='病例内容',max_length=500, blank=True, null=True)

    def model_name(self):
        return '病历'

    def __unicode__(self):
        return self.patient.user.username + "'s Record"