#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.signals import post_save

from ..accounts.models import User
from ..volunteer.models import Volunteer

SEX_CHOICES=(('1','男'),('0', '女'),('2','隐私'))

class Patient(models.Model):

    user = models.OneToOneField(User)
    sex = models.CharField(verbose_name='性别', default='2', choices=SEX_CHOICES, max_length=1)
    id_no = models.CharField(verbose_name='身份证号', max_length=18,blank=True, null=True)
    hometown=models.CharField(verbose_name='户籍地', max_length=10,blank=True, null=True)
    local = models.CharField(verbose_name='居住地', max_length=10,blank=True, null=True)

    onset_date = models.DateField(verbose_name='发病日期', blank=True, null=True)
    onset_causes = models.TextField(verbose_name='发病原因',blank=True, null=True)

    # 诊断医生 - 待做
    # 诊断医院 - 待做

    checklist = models.ImageField(verbose_name='检查单据', upload_to='patient/checklist',blank=True, null=True)
    # -- 个人描述 --
    disease_quality = models.TextField(verbose_name='病性',blank=True, null=True)
    mood = models.TextField(verbose_name='心情', max_length=140,blank=True, null=True)
    onset_process = models.TextField(verbose_name='发病过程',blank=True, null=True)


    def set_sex(self, s):
        if s == '1': self.sex='男'
        elif s == '0': self.sex='女'

    def get_sex(self):
        if self.sex == '1': return '男'
        elif self.sex == '0': return '女'
        else: return '隐私'

    def get_url(self):
        return '/patients/detail/%s/'%self.id

    def __unicode__(self):

        return self.user.username


def on_create(sender, instance, created, **kwargs):
    """ 创建用户的时候同步创建其他类型的用户
    """
    if created:
        print instance.is_patient
        if instance.is_patient:
            Patient.objects.create(user=instance)
        elif instance.is_volunteer:
            Volunteer.objects.create(user=instance)
        else:
            pass

post_save.connect(on_create, sender=User, weak=False,
          dispatch_uid='models.on_create')

