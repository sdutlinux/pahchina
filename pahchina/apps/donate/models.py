#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone

from ..accounts.models import User
# Create your models here.
class Donate(models.Model):

    number = models.CharField(max_length=15, unique=True, verbose_name='编号', blank=True)

    money = models.IntegerField(max_length=10, verbose_name='金额', help_text="单位: 元")
    residue = models.IntegerField(max_length=10, blank=True,verbose_name='剩余', help_text="单位: 元")

    create_time = models.DateTimeField(verbose_name='捐赠时间', auto_now_add=True)

    is_true = models.BooleanField(verbose_name='是否核实')
    mark_true_date = models.DateTimeField(verbose_name='核实时间', blank=True, null=True)

    user = models.ForeignKey(User, blank=True, null=True, verbose_name='捐赠用户')
    is_anonymous = models.BooleanField(verbose_name='是否匿名')

    detail = models.TextField(max_length=500, help_text='指明使用对象或地区，请不要超过500字。',
                               verbose_name='捐赠详情', blank=True, null=True)

    class Meta:
        verbose_name = '捐赠记录'

    def __unicode__(self):
        return "{} ({})".format(self.number, self.user)

    def get_anyone(self):
        if self.is_anonymous:
            return '匿名'
        else:
            return '非匿名'

    def get_status(self):
        return "已到帐" if self.is_true else "未到帐"

    def mark_true(self, status=True):
        """ 修改到帐
        """
        if status:
            self.is_true = True
            self.mark_true_date = timezone.now()
        else:
            self.is_true = False
            self.mark_true_date = None
            for _i in self.itemized_set.all():
                _i.delete()
            self.residue = self.money
        self.save()
        return True

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.number = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            self.residue = self.money
        super(Donate, self).save(force_insert=False, force_update=False, using=None,
                                 update_fields=None)


class Itemized(models.Model):

    donate = models.ForeignKey(Donate, verbose_name='所属捐赠条目', blank=True)

    created_user = models.ForeignKey(User, verbose_name='创建人', blank=True)
    created_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    cast = models.IntegerField(max_length='10', verbose_name='花费')
    detail = models.TextField(verbose_name='使用细节')
    
    class Meta:
        verbose_name = '捐赠使用记录'

    def delete(self, using=None):
        """ 重写删除方法，删除之后修改donate的余额
        """
        self.donate.residue += self.cast
        self.donate.save()
        super(Itemized, self).delete()

    #def save(self, force_insert=False, force_update=False, using=None,
    #         update_fields=None):
    #    # 修改剩余金额
    #    #self.donate.residue -= self.cast
    #    #self.donate.save()
    #    print update_fields
    #    super(Itemized, self).save(force_insert=False, force_update=False, using=None,
    #                               update_fields=None)
