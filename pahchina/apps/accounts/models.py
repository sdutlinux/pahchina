#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    1: patient, 患者
    2: doctor, 医生
    3: hospital, 医院
    4: donor, 捐献者
    5: volunteer, 志愿者
    6: druggist,  药商
    """
    avatar = models.ImageField(verbose_name='照片', upload_to='user/avatar',
                               blank=True, null=True)
    identity = models.CommaSeparatedIntegerField(verbose_name='身份类型',
                                                 max_length=10, blank=True, null=True)

    def set_patient(self):
        if '1' not in self.identity:
            self.identity += '1,'

    def del_patient(self):
        if '1,' in self.identity:
            self.identity.replace('1,','')

    def is_patient(self):
        if '1' in self.identity:
            return True
        else:
            return False


    def set_doctor(self):
        if '2' not in self.identity:
            self.identity += '2,'

    def del_doctor(self):
        if '2,' in self.identity:
            self.identity.replace('2,','')

    def is_doctor(self):
        if '2' in self.identity:
            return True
        else:
            return False


    def set_hospital(self):
        if '3' not in self.identity:
            self.identity += '3,'

    def del_hospital(self):
        if '3,' in self.identity:
            self.identity.replace('3,','')

    def is_hospital(self):
        if '3' in self.identity:
            return True
        else:
            return False


    def set_donor(self):
        if '4' not in self.identity:
            self.identity += '4,'

    def del_donor(self):
        if '4,' in self.identity:
            self.identity.replace('4,','')

    def is_donor(self):
        if '4' in self.identity:
            return True
        else:
            return False


    def set_volunteer(self):
        if '5' not in self.identity:
            self.identity += '5,'

    def del_volunteer(self):
        if '5,' in self.identity:
            self.identity.replace('5,','')

    def is_volunteer(self):
        if '5' in self.identity:
            return True
        else:
            return False


    def set_druggist(self):
        if '6' not in self.identity:
            self.identity += '6,'

    def del_druggist(self):
        if '6,' in self.identity:
            self.identity.replace('6,','')

    def is_druggist(self):
        if '6' in self.identity:
            return True
        else:
            return False
