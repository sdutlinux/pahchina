#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse

from ..accounts.models import User
from ..volunteer.models import Volunteer
from ..utils.models import TimeStampedModel

SEX_CHOICES=(('1','男'),('0', '女'),('2','隐私'))

class Patient(TimeStampedModel):

    user = models.OneToOneField(User)

    medical_history = models.TextField(verbose_name='病史', max_length=200,
                                       help_text='病情描述，叙述患病经过以及治疗和用药状况')
    # 初诊
    init_diag_hosp = models.CharField(verbose_name='初诊医院名称', max_length=50)
    init_diag_hosp_type = models.CharField(verbose_name='初诊医院类型', max_length=20,
                                           choices=(
                                               ("sjyy","省级医院"),
                                               ("xsjyy","县市级医院"),
                                               ("sqyy","社区医院"),
                                               ("xzyy","乡镇医院"),
                                               ("ncyy","农村医院"),
                                               ("srzs","私人诊所"),
                                               ("other","其他（请注明）"),
                                           ))
    init_diag_doct_conclu = models.TextField(verbose_name='初诊医生诊断结论', max_length=500)
    is_confirm = models.BooleanField(verbose_name='是否确认肺动脉高压',
                                     choices=((False,'否'),(True,'是')),default=False)
    why_not_confirm = models.CharField(verbose_name='未确诊原因', max_length=10,
                                       choices=(
                                           ("bqbyz","病情不严重"),
                                           ("jjyyzh","经济原因暂缓"),
                                           ("fcwhsyy","附近无合适医院"),
                                           ("other","其他（请注明）"),
                                       ),)

    # 确诊
    confirm_pah_date = models.DateField()
    #sex = models.CharField(verbose_name='性别', default='2', choices=SEX_CHOICES, max_length=1)
    #id_no = models.CharField(verbose_name='身份证号', max_length=18,blank=True, null=True)
    #hometown=models.CharField(verbose_name='户籍地', max_length=10,blank=True, null=True)
    #local = models.CharField(verbose_name='居住地', max_length=10,blank=True, null=True)

    onset_date = models.DateField(verbose_name='发病日期', blank=True, null=True)
    onset_causes = models.TextField(verbose_name='发病原因',blank=True, null=True)

    checklist = models.ImageField(verbose_name='检查单据', upload_to='patient/checklist',blank=True, null=True)
    # -- 个人描述 --
    disease_quality = models.TextField(verbose_name='病性',blank=True, null=True)
    mood = models.TextField(verbose_name='心情', max_length=140,blank=True, null=True)
    onset_process = models.TextField(verbose_name='发病过程',blank=True, null=True)

    class Meta:
        verbose_name = '患者'
        permissions = (
            ('my_doctor', 'Only my doctor can see'),
            ('my_hospital', 'Only my hospital can see'),
        )


    def get_doctor(self):
        return self.doctorrecord_set.get(end_date=None, patient=self).doctor

    def set_sex(self, s):
        if s == '1': self.sex='男'
        elif s == '0': self.sex='女'

    def get_sex(self):
        if self.sex == '1': return '男'
        elif self.sex == '0': return '女'
        else: return '隐私'

    def get_url(self):

        return reverse('admin-detail-patient', kwargs={'pk': self.id})

    def __unicode__(self):

        return self.user.username

class Drug(models.Model):

    name = models.CharField(verbose_name='药物名称', unique=True,
                            max_length=20, help_text='不能重复')
    description = models.TextField(verbose_name='药品描述')
    price = models.IntegerField(verbose_name='价格', max_length=10, help_text='单位为元(人民币)')

    def model_name(self):
        """ 用于某些时候描述这个model
        """
        return '药物'

    def __unicode__(self):

        return self.name

class Dosage(models.Model):
    """ 药物用量
    """

    drug = models.ForeignKey(Drug, verbose_name='药物名称')
    patient = models.ForeignKey(Patient, verbose_name='患者')

    dose = models.TextField(verbose_name='服药剂量', max_length=200,
                            help_text='描述使用该药的剂量，比如一月一盒等')

    datetime = models.DateTimeField(auto_now_add=True)

    def model_name(self):
        """ 用于某些时候描述这个model
        """
        return '药物用量记录'

    def __unicode__(self):

        return "%s使用%s的用量"% (self.patient, self.drug)
























































