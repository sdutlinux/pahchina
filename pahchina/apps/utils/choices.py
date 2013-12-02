#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

# 医生职称选择
DOCTOR_CHOICES = (
    ('zyys','住院医师'),
    ('zyzys','住院总医师'),
    ('zzys','主治医师'),
    ('fzrys','副主任医师'),
    ('zrys','主任医师'),
    ('js','讲师'),
    ('fjs','副教授'),
    ('jsh','教授'),
)

def get_full_desc(short, choices=DOCTOR_CHOICES):
    """ 通过简称获得全称
    """
    for i in choices:
        if i[0] == short:
            return i[1]
    return None