#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

from ..accounts.models import User


class Patient:

    user = models.OneToOneField(User, on_delete=True)
    sex = models.CharField(verbose_name='性别', default='隐私', choices=('男', '女', '隐私'))
    id_no = models.CharField(verbose_name='身份证号', max_length=18)
    hometown=models.CharField(verbose_name='户籍地', max_length=10)
    local = models.CharField(verbose_name='居住地', max_length=10)

    onset_date = models.DateField(verbose_name='发病日期')
    onset_causes = models.TextField(verbose_name='发病原因')

    # 诊断医生 - 待做
    # 诊断医院 - 待做

    photos = models.ImageField(verbose_name='照片', upload_to='patient/photo')
    checklist = models.ImageField(verbose_name='检查单据', upload_to='patient/checklist')

    # -- 个人描述 --

    disease_quality = models.TextField(verbose_name='病性')
    mood = models.TextField(verbose_name='心情', max_length=140)
    onset_process = models.TextField(verbose_name='发病过程')

    class Meta:
        ordering=['-date_joined']

    def set_sex(self, s):
        if s == 1: self.sex='男'
        elif s == 0: self.sex='女'

    def __unicode__(self):

        return self.user.username