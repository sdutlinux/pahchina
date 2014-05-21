#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from ..patient.models import Patient
from ..region.models import LivingRegion
from ..volunteer.models import Volunteer
from ..medical.models import Hospital, Doctor

def set_user_identity(user, key):
    """ 为用户设置角色
    """
    _dic = {
        'patient': Patient,
        'doctor': Doctor,
        'hospital': Hospital,
        'volunteer': Volunteer,
        # 5: ('druggist')
    }
    if 'patient' == key: user.is_patient = True
    if 'doctor' == key: user.is_doctor = True
    if 'hospital' == key: user.is_hospital = True
    if 'volunteer' == key: user.is_volunteer = True
    _dic[key].objects.create(user=user)
    return True


def set_user_region(user, cate, province, city, area):
    """ 设置用户住址
    """
    _region = LivingRegion.objects.get_or_create(user_id=user.id, cate=cate)[0]
    _region.province, _region.city, _region.area = province, city, area
    _region.save()
    return _region