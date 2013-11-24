#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from ..accounts.models import User
# Create your models here.
class Volunteer(models.Model):
    SEX = (
        ('M', 'MAN'),
        ('W', 'WOMAN'),
    )
    user = models.OneToOneField(User, on_delete=True, verbose_name='姓名')
    sex = models.CharField(max_length=1, choices=SEX, verbose_name='性别')
    specialty = models.CharField(max_length=100, blank=True, null=True, verbose_name='个人专长') #专长
    aspiration = models.CharField(max_length=50, blank=True, null=True, verbose_name='个人意愿')
    liveness = models.IntegerField(verbose_name='活跃度') #活跃度
    #联系方式
    phone = models.CharField(max_length=11, verbose_name='联系手机')
    address = models.CharField(max_length=50, blank=True, null=True, verbose_name='住址')

    class Meta:
        verbose_name = '志愿者'
        verbose_name_plural = '志愿者'

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
