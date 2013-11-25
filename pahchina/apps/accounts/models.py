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

    identity_dic = {
        'is_patient':'1,',
        'is_doctor': '2,',
        'is_hospital': '3,',
        'is_donor': '4,',
        'is_volunteer': '5,',
        'is_druggist': '6,',
    }

    def get_absolute_url(self):
        """ 获取用户URL
        用户后台的用户管理
        """
        return '/accounts/user/%s' % self.id

    def get_identity(self):
        """ 返回具体身份名称
        """
        res = ''
        if self.is_donor: res += '捐献者、'
        if self.is_volunteer: res += '志愿者、'
        if self.is_doctor: res += '医生、'
        if self.is_druggist: res += '药商、'
        if self.is_hospital: res += '医院、'
        if self.is_patient: res += '患者、'
        if self.is_staff: res = '分站管理员、'
        if self.is_superuser: res = '总站管理员、'
        return res

    def __getattr__(self, item):
        """ 用来判断身份
        item: is_patient, is_doctor, ...
        """
        if item in self.identity_dic and item.startswith('is_'):
            # 判断非属性并且以 `is_`开头
            if self.identity_dic[item] in self.identity:
                return True
            else:
                return False
        else:
            super(User, self).__getattr__(item)

    def __setattr__(self, key, value):
        """ 用来设置用户身份
        Usage: self.is_patient = True
        设定的值只允许为True, 其它值抛出异常。
        """
        if key in self.identity_dic and key.startswith('is_'):
            if self.identity_dic[key] not in self.identity and value is True:
                self.identity += self.identity_dic[key]
                self.save(update_fields=["identity"])
            else:
                raise Exception('Value not permit, Just allow `True`')
        else:
            # 不符合条件时调用父类的该方法，避免AttributeError
            super(User, self).__setattr__(key, value)

    def __delattr__(self, item):
        """ 用于删除用户身份
        Usage: del self.is_patient, ....
        """
        if item in self.identity_dic:
            if self.identity_dic[item]+',' in self.identity:
                self.identity = self.identity.replace(self.identity_dic[item], '')
                self.save(update_fields=["identity"])
            else:
                raise Exception('User is not %s'%self.identity_dic[item][3:])
        else:
            super(User, self).__delattr__(item)
