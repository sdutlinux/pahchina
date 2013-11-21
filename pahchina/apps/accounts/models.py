#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    is_patient=models.BooleanField(default=False,)  # 患者
    is_doctor=models.BooleanField(default=False)    # 医生
    is_hospital=models.BooleanField(default=False)  # 医院
    is_donor=models.BooleanField(default=False)     # 捐献者
    is_volunteer=models.BooleanField(default=False) # 志愿者