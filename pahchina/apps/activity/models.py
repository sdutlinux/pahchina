#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from ..volunteer.models import Volunteer
# Create your models here.

class Activity:
    name = models.CharField(max_length=20,verbose_name='活动名称')
    activity_time = models.DateTimeField(verbose_name='活动时间')
    place = models.CharField(verbose_name='活动地点')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    #成员
    verlunteer = models.ManyToManyField(Volunteer, verbose_name='参加志愿者')
    patient = models.ManyToManyField(verbose_name='参加患者')
    describe = models.TextField(verbose_name='活动描述')
    remarks = models.TextField(verbose_name='活动备注', blank=True, null=True)
