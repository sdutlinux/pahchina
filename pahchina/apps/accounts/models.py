#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    is_patient=models.BooleanField(verbose_name='是否患者',default=False,help_text='hello world')  # 患者
    is_doctor=models.BooleanField(verbose_name='是否医生',default=False)    # 医生
    is_hospital=models.BooleanField(verbose_name='是否医院',default=False)  # 医院
    is_donor=models.BooleanField(verbose_name='是否捐献者',default=False)     # 捐献者
    is_volunteer=models.BooleanField(verbose_name='是否志愿者',default=False) # 志愿者
    is_druggist=models.BooleanField(verbose_name='是否药商', default=False)    # 药商