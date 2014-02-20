#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.db import models
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

from ..utils.models import TimeStampedModel
from ..utils.choices import DOCTOR_CHOICES, get_full_desc
from ..accounts.models import User
from ..patient.models import SEX_CHOICES, Patient


class Hospital(models.Model):

    user = models.OneToOneField(User, verbose_name='医院名称')
    local = models.CharField(verbose_name='所在地区', max_length=20)
    is_community = models.BooleanField(verbose_name='是否治疗中心')
    level = models.CharField(verbose_name='医院等级', max_length=20)

    class Meta:
        verbose_name = '医生'

    def __unicode__(self):
        return self.user.username


class Doctor(models.Model):

    user = models.OneToOneField(User, verbose_name='医生姓名')
    hospital = models.ForeignKey(Hospital, verbose_name='所在医院', blank=True, null=True)

    sex = models.CharField(verbose_name='性别', default='2', choices=SEX_CHOICES, max_length=1)
    age = models.CharField(verbose_name='年龄', max_length=2, blank=True, null=True)

    job_title = models.CharField(verbose_name='职称', max_length=10, blank=True, null=True,
                                 choices=DOCTOR_CHOICES)

    class Meta:
        verbose_name = '医生'

    def get_sex(self):
        if self.sex == '1': return '男'
        elif self.sex == '0': return '女'
        else: return '隐私'

    def get_patients(self):
        """ 通过就医记录获取患者列表
        """
        record_list = self.doctorrecord_set.filter(end_date=None, doctor=self)
        for r in record_list:
            yield r.patient

    def get_job_title(self):
        """ 获取医生职称
        """
        return get_full_desc(self.job_title, choices=DOCTOR_CHOICES)

    def __unicode__(self):
        return self.user.username


class Record(TimeStampedModel):
    """ 患者的病情记录
    More: 此处可用 **unique_for_？？** 来限制病例的创建频率
    """
    patient = models.ForeignKey(Patient, verbose_name='病人', blank=True)
    doctor = models.ForeignKey(Doctor, verbose_name='检查医师')
    type = models.CharField(verbose_name='记录类型', max_length=10,
                            choices=(("description","病情描述"),("result","检查结果"),),
                            help_text='病情描述、检查结果数据')
    physical_state = models.CharField(verbose_name='最近身体状况', max_length=10,
                                      choices=(
                                          ("badly","非常不好"),
                                          ("worse","不太好"),
                                          ("stable","稳定"),
                                          ("better","有改善"),
                                          ("nice","改善明显"),
                                      ))
    mental_state = models.CharField(verbose_name='最近精神状态', max_length=10,
                                    choices=(
                                        ("zshbg","总是很悲观"),
                                        ("jchbg","经常很悲观"),
                                        ("oeng","偶尔难过"),
                                        ("ddlg","大多数时间乐观"),
                                        ("zslg","总是很乐观"),
                                    ))
    living_state = models.CharField(verbose_name='目前生活状况', max_length=10,
                                        choices=(
                                            ("zcgz","基本正常工作"),
                                            ("gzcl","工作很吃力"),
                                            ("sbzl","不工作生活自理"),
                                            ("shbnzl","生活不能自理"),
                                        ))
    present_symptoms = models.CharField(verbose_name='目前症状及体征', max_length=30,
                                        choices=(
                                            ("xmqd","胸闷气短"),
                                            ("xt","胸痛"),
                                            ("kx","咳血"),
                                            ("pwjghxkn","平卧即感呼吸困难"),
                                            ("zg","紫绀"),
                                            ("xj","心悸"),
                                            ("jrtt","肌肉疼痛"),
                                            ("xzhfbfz","下肢或腹部浮肿"),
                                            ("exot","恶心呕吐"),
                                            ("other","其他症状（请描述）"),
                                        ),
                                        blank=True, null=True)

    present_heart_func = models.CharField(verbose_name='目前心功能', max_length=20,
                                          choices=(
                                              ("1","I级"),
                                              ("2","II级"),
                                              ("3","III级"),
                                              ("4","IV级"),
                                          ),)

    check_item = models.CharField(verbose_name='检查项目', max_length=20,
                                  choices=(
                                      ("ggn","肝功能"),
                                      ("sgn","肾功能"),
                                      ("xgn","心功能"),
                                      ("cc","彩超"),
                                      ("other","其他(请列明)"),
                                  ))
    pap = models.CharField(verbose_name='肺动脉压力', max_length=10,
                           help_text='单位：mmHg')
    heart_fail_value = models.CharField(verbose_name='心衰值', max_length=10)

    walk_distance_in6 = models.PositiveIntegerField(verbose_name='6分钟步行距离',
                                                help_text='单位：（米）',
                                                blank=True, null=True)
    bp = models.CharField(verbose_name='血压', max_length=20,
                          help_text='单位：mmHg')
    glu = models.CharField(verbose_name='血糖', max_length=20,
                           help_text='单位：mmol/L，正常值：3.61~6.11mmol/L')
    chol = models.CharField(verbose_name='胆固醇', max_length=20,
                            help_text='单位：，正常值：2.4--5.5mmol/L')
    ua = models.CharField(verbose_name='尿酸', max_length=20,
                          help_text='单位：umol/L，正常值：男149~416umol/L；女89~357umol/L；')


    class Meta:
        verbose_name = '病情记录'

    def __unicode__(self):
        return self.patient.user.username + "'s 病情记录"


class DoctorRecord(models.Model):
    """ 患者就医记录
    患者患病后经过那些医生的诊治
    """

    patient = models.ForeignKey(Patient, verbose_name='患者', blank=True)
    doctor = models.ForeignKey(Doctor, verbose_name='医生')

    from_date = models.DateTimeField(verbose_name='开始日期', auto_now_add=True)
    from_description = models.TextField(verbose_name='就医说明', max_length=500)

    end_date = models.DateTimeField(verbose_name='结束日期', blank=True, null=True)
    end_description = models.TextField(verbose_name='结束说明', max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = '患者就医记录'

    def status(self):
        if self.end_date:return '已结束'
        else:return '正在接受治疗'

    def __unicode__(self):
        return self.patient.user.username + ' Doctor History'









