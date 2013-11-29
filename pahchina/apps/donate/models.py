#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.db import models
from ..accounts.models import User
# Create your models here.
class Donate(models.Model):
    number = models.CharField(max_length=15, unique=True,verbose_name='编号', blank=True)
    money = models.IntegerField(max_length=10, verbose_name='金额')
    create_time = models.DateTimeField(verbose_name='捐赠时间', auto_now_add=True)
    true_time = models.DateTimeField(verbose_name='核实时间', blank=True, null=True)
    isanonymous = models.BooleanField(verbose_name='是否匿名')
    istrue = models.BooleanField(verbose_name='是否核实')
    user = models.ForeignKey(User,blank=True, null=True, verbose_name='捐赠用户')
    details = models.TextField(max_length=500, help_text='请不要超过500字。', verbose_name='捐赠详情', blank=True, null=True)

    def get_anyone(self):
        if self.isanonymous:return '匿名'
        else:return '非匿名'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.number = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        super(Donate, self).save(force_insert=False, force_update=False, using=None,
             update_fields=None)
