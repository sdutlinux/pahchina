#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.db.models.signals import post_save

from ..accounts.models import User
from ..patient.models import Patient
from ..volunteer.models import Volunteer

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