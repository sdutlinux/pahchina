#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from ..patient.models import Patient
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
    user.__setattr__("is_"+key, True)
    _dic[key].objects.create(user=user)
    return True