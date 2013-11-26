#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from ..accounts.models import User
# Create your models here.
class Volunteer(models.Model):
    SEX = (
        ('M', '男'),
        ('W', '女'),
        ('UK', '隐私')
    )
    user = models.OneToOneField(User, on_delete=True, verbose_name='姓名')
    sex = models.CharField(max_length=1, choices=SEX, verbose_name='性别', default='UK')
    specialty = models.CharField(max_length=100, blank=True, null=True, verbose_name='个人专长') #专长
    aspiration = models.CharField(max_length=50, blank=True, null=True, verbose_name='个人意愿')
    liveness = models.IntegerField(verbose_name='活跃度', default=0) #活跃度
    #联系方式
    phone = models.CharField(max_length=11, verbose_name='联系手机', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name='住址')

    def get_sex(self):
        if self.sex == 'M': return '男'
        elif self.sex == 'W': return '女'
        else: return '隐私'


    def __unicode__(self):
        return self.user.username


'''
class Active:
    time = models.DateField()
    site = models.CharField() #
    volunteer = models.ManyToManyField(Volunteer)
    #patient = models.ManyToManyField()
    describe = models.TextField()
'''
