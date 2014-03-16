#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
#from django.contrib.sites.models import Site, RequestSite
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.core.validators import RegexValidator

from ..utils import TimeStampedModel
from ..accounts.models import User
#from ..region.models import LivingRegion


class Website(TimeStampedModel):
    """ 站点必要信息
    添加： 站点管理员、描述
    """
    #site = models.OneToOneField(Site)
    name = models.CharField(verbose_name='站点名称', max_length=50)
    domain = models.CharField(verbose_name='域名',
                              validators=[RegexValidator('^([a-z0-9]+\.[a-z0-9]|[a-z0-9])+\.[a-z]{1,5}$','输入格式错误','输入格式错误')],
                              help_text='仅输入域名，eg: example.com',
                              max_length=40)

    logo = models.ImageField(verbose_name='网站Logo', upload_to='sites/logo')
    cut = models.ImageField(verbose_name='网站图片', upload_to='sites/cut', blank=True, null=True,
                            help_text='简介版块调用')

    admin = models.OneToOneField(User, verbose_name='站点管理员',
                                 #choices=[(u.id,u.username) for u in User.objects.filter(is_staff=True)],
                                 help_text='只有管理员用户可选<a href="/accounts/list/user">添加管理员</a>')

    address = models.CharField(verbose_name='地址', max_length=200)
    description = models.TextField(verbose_name='网站简介', max_length=300,
                                   help_text='联盟、地方病友会简介')

    contact_name = models.CharField(verbose_name='联系人', max_length=10, blank=True, null=True,
                                    help_text='若不填写则显示站点管理员姓名')
    telephone = models.CharField(verbose_name='联系电话', max_length=13, blank=True, null=True,
                                 help_text='若不填写则显示站点管理员的联系电话')
    qq = models.CharField(verbose_name='官方QQ', max_length=11, blank=True, null=True)



    class Meta:
        verbose_name = '站点'

    def __unicode__(self):
        return "%s(%s)"%(self.name,self.domain)

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

    #def get_users(self):
    #    """站点获取属于当前站点的用户
    #    通过用户的户籍地或者居住地获取
    #    暂时使用居住地
    #    """
    #    region_list = self.region_set.all()
    #    user_list =


#def get_current_site(request):
#    """
#    Checks if contrib.sites is installed and returns either the current
#    ``Site`` object or a ``RequestSite`` object based on the request.
#    """
#    #if Site._meta.installed:
#    domain=request.get_host().split(":")[0]
#    print domain
#    if domain in ('127.0.0.1', '0.0.0.0'):
#        current_site=get_object_or_404(Site, id=1)
#    else:
#        current_site = get_object_or_404(Site, domain=domain)
#    #print site
#    #current_site = get_object_or_404(SiteProfile, site=site)
#    #current_site = site.siteprofile
#    #else:
#    #    current_site = RequestSite(request)
#    return current_site
