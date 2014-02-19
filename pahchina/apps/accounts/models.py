#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse, reverse_lazy

IDENTITY_CHOICES = ((0,'无'), (1,'患者'), (2, '医生'),
                    (3,'医院'),(4, '志愿者'), (5, '药商'),)

class User(AbstractUser):
    """用户类
    自定义了django默认的用户系统
    增加了下面两个字段以及一些常用方法
    """
    avatar = models.ImageField(verbose_name='照片', upload_to='user/avatar',
                               blank=True, null=True)

    telephone = models.CharField(verbose_name='联系电话', max_length=13)

    identity = models.SmallIntegerField(verbose_name='身份类型', default=0, choices=IDENTITY_CHOICES,
                                        max_length=1)

    identity_dic = {
        'is_patient':1,
        'is_doctor': 2,
        'is_hospital': 3,
        'is_volunteer': 4,
        'is_druggist': 5,
    }

    def get_absolute_url(self):
        """ 获取用户URL
        用户后台的用户管理
        """
        return reverse('admin-detail-user', kwargs={'pk': self.id})

    def get_profile_url(self):
        """ 返回个人主页链接
        """
        #if not self.is_staff:
        return reverse_lazy('profile')
        #return reverse_lazy('index')

    def get_show_url(self):
        """ 获取展示页面URL
        """
        return reverse('show', kwargs={'pk': self.id})

    def get_identity(self):
        """ 返回身份名称
        eg: 患者，志愿者等
        """
        res = None

        for i in IDENTITY_CHOICES:
            if i[0] == self.identity:
                res = i[1]
        if self.is_staff: res += ', 分站管理员'
        if self.is_superuser: res = '总站管理员'
        return res

    def get_full_name(self):
        """ 符合中文姓名风格
        """
        full_name = '%s%s' % (self.last_name, self.first_name)
        return full_name.strip()

    def __getattr__(self, item):
        """ 用来判断身份
        item: is_patient, is_doctor, ...
        """
        if item in self.identity_dic and item.startswith('is_'):
            # 判断非属性并且以 `is_`开头
            if self.identity_dic[item] == self.identity:
                return True
            else:
                return False
        else:
            super(User, self).__getattr__(item)






#个人资料
#class Personal(models.Model):
#    previous_name = models.CharField(verbose_name='曾用名')
#    nickname = models.CharField(verbose_name='昵称')
#    sex = models.CharField(choices=('man','woman'))
#    ID_number = models.CharField(verbose_name='')
#    age = models.IntegerField('')
#    birthday = models.DateField('')
#    nationality = models.CharField(verbose_name='')
#    belief = models.CharField(verbose_name='')
#    height = models.DecimalField(verbose_name='')
#    weight = models.DecimalField(verbose_name='')
#    marital_status = models.CharField(verbose_name='',choices=(''))
#    bear_status = models.CharField(verbose_name='',choices=())
#    home_phone = models.CharField(verbose_name='')
#    domicile = models.CharField(verbose_name='')
#    permanent_residence = models.CharField(verbose_name='')
#    address = models.CharField(verbose_name='')
#    education = models.CharField(verbose_name='',choices=())
#    school = models.CharField(verbose_name='')
#    major = models.CharField(verbose_name='')
#    qualification = models.CharField(verbose_name='')
#    specialty = models.CharField(verbose_name='')




