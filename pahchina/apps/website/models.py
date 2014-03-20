#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.forms.models import model_to_dict
from django.core.validators import RegexValidator

from tinymce import models as tiny_models

from ..utils import TimeStampedModel
from ..accounts.models import User
#from ..region.models import LivingRegion


class Website(TimeStampedModel):
    """ 站点必要信息
    添加： 站点管理员、描述
    """
    # 站点基本信息
    name = models.CharField(verbose_name='站点名称', max_length=50)
    domain = models.CharField(verbose_name='域名',
                              validators=[RegexValidator('^([a-z0-9]+\.[a-z0-9]|[a-z0-9])+\.[a-z]{1,5}$','输入格式错误','输入格式错误')],
                              help_text='仅输入域名，eg: example.com',
                              max_length=40)
    logo = models.ImageField(verbose_name='网站Logo', upload_to='sites/logo')
    cut = models.ImageField(verbose_name='网站图片', upload_to='sites/cut', blank=True, null=True,
                            help_text='简介版块调用')
    # 联系信息
    admin = models.OneToOneField(User, verbose_name='站点管理员',
                                 #choices=[(u.id,u.username) for u in User.objects.filter(is_staff=True)],
                                 help_text='只有管理员用户可选<a href="/accounts/list/user">添加管理员</a>')
    contact_name = models.CharField(verbose_name='联系人', max_length=10, blank=True, null=True,
                                    help_text='若不填写则显示站点管理员姓名')
    telephone = models.CharField(verbose_name='联系电话', max_length=13, blank=True, null=True,
                                 help_text='若不填写则显示站点管理员的联系电话')
    qq = models.CharField(verbose_name='官方QQ', max_length=11, blank=True, null=True)
    address = models.CharField(verbose_name='地址', max_length=200)

    # 展示使用
    description = models.TextField(verbose_name='网站简介', max_length=300,
                                   help_text='联盟、地方病友会简介')
    #notice = models.TextField(verbose_name='站点公告', max_length=300,
    #                          help_text='网站最新动态或活动')
    notice = tiny_models.HTMLField(verbose_name='站点公告', max_length=300,
                              help_text='网站最新动态或活动')



    class Meta:
        verbose_name = '站点'

    def __unicode__(self):
        return "%s(%s)"%(self.name,self.domain)

    def link(self):
        return "http://{}".format(self.domain)

    def get_level(self):
        """ 获取网站等级
        ret: 总站、分站
        """
        return '总站' if self.id == 1 else '地方分站'

    def get_dict(self):

        return model_to_dict(self)

    def get_cut_url(self):

        return self.cut.url if self.cut else ''

    def get_contact(self):
        """ 获取站点联系人
        """
        return self.contact_name or self.admin.username

    def get_telephone(self):
        """ 返回联系电话
        """
        return self.telephone or self.admin.telephone



class Links(models.Model):
    """ 友情链接
    """
    site = models.ForeignKey(Website, verbose_name='所属站点')

    name = models.CharField(max_length=20,verbose_name='站点名称', help_text='最长20个字符')

    url = models.URLField(verbose_name='站点网址',max_length=64)

    class Meta:
        verbose_name = "友情链接"

    def __unicode__(self):
        return "{}[{}]".format(self.name, self.url)
