#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from django.db import models
from django.utils.timezone import datetime, now as django_now
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse, reverse_lazy

IDENTITY_CHOICES = ((0, '普通用户'), (1, '患者'), (2, '医生'),
                    (3, '医院'), (4, '志愿者'), (5, '药商'),)
IDENTITY_LIST = ('patient', 'doctor', 'hospital', 'volunteer')

class User(AbstractUser):
    """用户类
    自定义了django默认的用户系统
    增加了下面两个字段以及一些常用方法
    """

    #基本信息
    mark = models.TextField(verbose_name="标记信息", default="{}",null=True, blank=True)
    # 用作标记必要信息，可能会保存成JSON或其他格式

    spare = models.EmailField(blank=True, null=True,
                              verbose_name='备用邮箱',
                              help_text='')
    cellphone = models.CharField(verbose_name='常用手机', max_length=12,
                              help_text='验证账号，找会密码用')

    spare_phone = models.CharField(blank=True, null=True, max_length=12,
                                   verbose_name='备用手机',
                                   help_text='')
    qq = models.CharField(verbose_name='QQ号',
                          max_length=20,
                          help_text='')
    score = models.BigIntegerField(verbose_name='积分',
                                   default=0,
                                   help_text='完善资料，填写问卷得积分')
    remark = models.TextField(blank=True, null=True,
                              verbose_name='管理员备注',
                              help_text='管理员记录备注信息')
    # 登录次数
    login_times = models.IntegerField(verbose_name='登录次数',
                                      default=0,
                                      help_text='')
    login_times_week = models.IntegerField(default=0,
                                           verbose_name='周登录次数',
                                           help_text='')
    login_times_month = models.IntegerField(default=0,
                                            verbose_name='月登录次数',
                                            help_text='')

    avatar = models.ImageField(verbose_name='照片', upload_to='user/avatar',
                               blank=True, null=True)

    telephone = models.CharField(verbose_name='联系电话', max_length=13)

    identity = models.CharField(verbose_name='身份类型', default="", max_length=100)

    def __unicode__(self):
        return self.username

    def get_avatar_url(self):
        """ 返回头像链接，无则返回默认头像链接
        """
        if self.avatar:
            return self.avatar.url
        else:
            return "/static/img/default_avatar.png"

    def count_login_time(self):
        from django.utils import timezone
        _timedelta = timezone.now() - self.last_login
        if _timedelta.total_seconds() >= 3600:
            # 两次登录之间超过一小时才计入
            self.login_times += 1
            self.save()
        return True

    def get_absolute_url(self):
        """ 获取用户URL
        用户后台的用户管理
        """
        return reverse('admin-update', kwargs={'model':'user',
                                               'pk': self.id})

    def get_info_rate(self):
        """ 个人资料完整度
        返回结果：0-1 (int)
        未完成
        """
        return 1

    def get_profile_url(self):
        """ 返回个人主页链接
        """
        #if not self.is_staff:
        return reverse_lazy('profile')
        #return reverse_lazy('index')

    def get_show_url(self):
        """ 获取展示页面URL
        """
        return reverse('show', kwargs={'username': self.username})

    def get_apartment(self):
        """ 返回居住信息"""
        return self.livingregion_set.get(cate="apartment").get_location()

    def get_household(self):
        """返回户籍信息"""
        return self.livingregion_set.get(cate='household').get_location()

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

    def get_identity_model(self):
        """ 返回角色model
        """
        if self.is_patient: return self.patient
        elif self.is_doctor: return self.doctor
        elif self.is_hospital: return self.hospital
        elif self.is_volunteer: return self.volunteer
        return self



    def get_full_name(self):
        """ 符合中文姓名风格 """
        full_name = '%s%s' % (self.last_name, self.first_name)
        return full_name.strip()

    def set_mark(self, key, value):
        """数据库中的键值对"""
        obj=json.loads(self.mark)
        if value=="delete": obj.pop(key)
        else: obj[key]=value
        self.mark=json.dumps(obj)
        self.save()
    def get_mark(self, key):
        """获取值"""
        obj = json.loads(self.mark)
        return obj.get(key, None)

    def __getattr__(self, item):
        """ 用来判断身份
        item: is_patient, is_doctor, ...
        """
        if item.startswith('is_') and item[3:] in IDENTITY_LIST:
            if item[3:] in self.identity.split("_"):
                return True
            else: return False
        else:
            return super(User, self).__getattr__(item)

    def __setattr__(self, item, value):
        """ 用来判断身份
        item: is_patient, is_doctor, ...
        """
        if item.startswith('is_') and item[3:] in IDENTITY_LIST:
            if value is True:
                self.identity += item[2:]
                print "set true"
            else:
                if self.__getattr__(item):
                    _identity_list = self.identity.split("_")
                    _identity_list.remove(item[3:])
                    print "set false"
                    self.identity = "_".join(_identity_list)
            self.save()
        else:
            return super(User, self).__setattr__(item, value)


# choices

SEX_CHOICES = (
    ('MAN', '男'),
    ('WOMAN', '女'),
)
MARITAL_CHOICES = (
    ('SINGLE', '单身'),
    ('MARRIED', '有配偶'),
    ('WIDOWED', '丧偶'),
    ('DIVORCE', '离异'),
)
EDUCATION_CHOICES = (
    ('PRIMARY', '小学'),
    ('JUNIOR', '初中'),
    ('HIGH', '高中'),
    ('UNIVERSITY', '大学'),
    ('GRADUATE', '研究生'),
)


class Personal(models.Model):

    user=models.OneToOneField(User, blank=True)
    #不可修改
    previous_name = models.CharField(verbose_name='曾用名',
                                     max_length=20,
                                     help_text='无则填“无”')

    nickname = models.CharField(verbose_name='昵称',
                                max_length=20,
                                help_text='')

    sex = models.CharField(verbose_name='性别',
                           choices=SEX_CHOICES,
                           max_length=20,
                           help_text='男｜女，选择')

    ID_number = models.CharField(verbose_name='身份证号',
                                 max_length=20,
                                 help_text='唯一性，提交后不可更改')
    #志愿者可修改，
    age = models.IntegerField(verbose_name='年龄', default=0,
                              help_text='')

    birthday = models.DateField(verbose_name='生日',
                                help_text='',
                                blank=True, null=True)
#个人捐赠者可修改
    nationality = models.CharField(verbose_name='民族',
                                       max_length=20,
                                   help_text='选，汉族，少数民族',
                                   blank=True, null=True)

    belief = models.CharField(verbose_name='信仰',
                              max_length=20,
                              help_text='无，马列，佛，基督，其他',
                              blank=True, null=True)

    height = models.DecimalField(verbose_name='身高',
                                 decimal_places=2,
                                 max_digits=5,
                                 blank=True, null=True)

    weight = models.DecimalField(verbose_name='体重',
                                 decimal_places=2,
                                 max_digits=5,
                                 blank=True, null=True)

    marital_status = models.CharField(verbose_name='婚姻状态',
                                      choices=MARITAL_CHOICES,
                                      max_length=20,
                                      blank=True, null=True)

    bear_status = models.BooleanField(verbose_name='是否生育',
                                      max_length=20, help_text='',
                                      default=False)

    home_phone = models.CharField(verbose_name='家庭电话',
                                  max_length=20,
                                  blank=True, null=True)

    address = models.CharField(verbose_name='通信地址',
                               max_length=20,
                               help_text='用于邮寄杂志或者资料物品等',
                               blank=True, null=True)

    education = models.CharField(verbose_name='最高学历',
                                 choices=EDUCATION_CHOICES,
                                 max_length=20,
                                 blank=True, null=True)

    school = models.CharField(verbose_name='毕业院校',
                              max_length=20,
                              blank=True, null=True,
                              help_text='填学校名称')

    major = models.CharField(verbose_name='专业',
                             max_length=20,
                             blank=True, null=True,
                             help_text='填写专业名称')

    qualification = models.CharField(verbose_name='执业资格证',
                                     max_length=20,
                                     help_text='律师，会计，心理咨询师',
                                     blank=True, null=True)

    specialty = models.CharField(verbose_name='特长爱好',
                                 max_length=20,
                                 help_text='琴棋书画',
                                 blank=True, null=True)
    personal_profile = models.TextField(verbose_name='个人简介',
                                        blank=True, null=True,
                                        help_text='医生、志愿者用，网站调用')
    story = models.TextField(verbose_name='患者故事',
                             blank=True, null=True,
                             help_text='患者自述')

    def get_birthday(self):
        """  通过身份证号获取生日
        """
        try:
            date = datetime.strptime(self.ID_number[6:14], "%Y%m%d")
            return date
        except IndexError:
            return None

    def get_age(self):
        """ 通过身份证号获取年龄
        """
        if isinstance(self.get_birthday(), datetime):
            age = django_now().year - self.get_birthday().year
            return age


#单位资料

#choise
STATUS_CHOICES = (
    ('YES', '在业'),
    ('NO', '不在业'),
    ('TEMPORARY', '临时工'),
)
NATURE_CHOICES = (
    ('GOVERNMENT', '政府机关'),
    ('STATE-OWNED_ENTERPRISE', '国营企业'),
    ('INSTITUTION', '事业单位'),
    ('PRIVATE_ENTERPRISE', '民营企业'),
)
HOSPITAL_LV_SHOICES = (
    ('1', '一级'),
    ('2', '二级'),
    ('3', '三级'),
    ('4', '四级')
)


class Unit(models.Model):
    user=models.OneToOneField(User, blank=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=20,
                              verbose_name='工作状态',
                              help_text='选择',
                              blank=True, null=True)
    occupation = models.CharField(max_length=20,
                                  verbose_name='职业',
                                  help_text='若又工作，则填写相关资料',
                                  blank=True, null=True)
    nature = models.CharField(choices=NATURE_CHOICES,
                              max_length=30,
                              verbose_name='单位性质',
                              help_text='请选择',
                              blank=True, null=True)
    annual_income = models.CharField(max_length=20,
                                     verbose_name='年收入',
                                     help_text='',
                                     blank=True, null=True)

    name = models.CharField(max_length=20,
                            verbose_name='单位名称',
                            help_text='',
                            blank=True, null=True)
    department = models.CharField(max_length=20,
                                  verbose_name='所在部门',
                                  help_text='',
                                  blank=True, null=True)
    post = models.CharField(max_length=20,
                            verbose_name='职务',
                            help_text='',
                            blank=True, null=True)
    title = models.CharField(max_length=20,
                             verbose_name='职称',
                             help_text='',
                             blank=True, null=True)
    province = models.CharField(max_length=20,
                                verbose_name='所在省份',
                                help_text='用于分地区统计和网站展示',
                                blank=True, null=True)
    city = models.CharField(max_length=20,
                            verbose_name='所在城市',
                            help_text='',
                            blank=True, null=True)
    address = models.CharField(max_length=20,
                               verbose_name='地址',
                               help_text='',
                               blank=True, null=True)
    phone = models.CharField(max_length=20,
                             verbose_name='电话',
                             help_text='',
                             blank=True, null=True)
    fax = models.CharField(max_length=20,
                           verbose_name='传真',
                           help_text='',
                           blank=True, null=True)
    web_site = models.CharField(max_length=20,
                                verbose_name='网站',
                                help_text='',
                                blank=True, null=True)
    # logo = models.ImageField(verbose_name='机构logo',help_text='',blank=True,null=True)
    # photo = models.ImageField(verbose_name='机构图片',help_text='')
    introduce = models.TextField(verbose_name='机构简介',
                                 help_text='',
                                 blank=True, null=True)
    #联系人信息
    # 姓名，性别，与病人关系，联系人职务，联系人电话，联系人手机，联系人邮箱，联系人QQ


class Bank(models.Model):
    user=models.OneToOneField(User, blank=True)
    name = models.CharField(max_length=20,
                            verbose_name='户名',
                            help_text='',
                            blank=True, null=True)
    area = models.CharField(max_length=20,
                            verbose_name='开户地区',
                            help_text='XX省XX市XX县',
                            blank=True, null=True)
    bank_name = models.CharField(max_length=20,
                                 verbose_name='开户银行',
                                 help_text='XXX银行XXX分行XXX支行',
                                 blank=True, null=True)
    number = models.CharField(max_length=20,
                              verbose_name='银行账号',
                              help_text='',
                              blank=True, null=True)