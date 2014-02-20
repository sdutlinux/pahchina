#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse

from ..accounts.models import User
from ..volunteer.models import Volunteer
from ..utils.models import TimeStampedModel
#from ..medical.models import Doctor

SEX_CHOICES=(('1','男'),('0', '女'),('2','隐私'))

class Patient(TimeStampedModel):

    user = models.OneToOneField(User, blank=True)

    medical_history = models.TextField(verbose_name='病史', max_length=200,
                                       help_text='病情描述，叙述患病经过以及治疗和用药状况',
                                       blank=True, null=True)
    # 初诊
    init_diag_hosp = models.CharField(verbose_name='初诊医院名称', max_length=50,
                                      blank=True, null=True)
    init_diag_hosp_type = models.CharField(verbose_name='初诊医院类型', max_length=20,
                                           choices=(
                                               ("sjyy","省级医院"),
                                               ("xsjyy","县市级医院"),
                                               ("sqyy","社区医院"),
                                               ("xzyy","乡镇医院"),
                                               ("ncyy","农村医院"),
                                               ("srzs","私人诊所"),
                                               ("other","其他（请注明）"),
                                           ),
                                           blank=True, null=True)
    init_diag_doct_conclu = models.TextField(verbose_name='初诊医生诊断结论', max_length=500,
                                             blank=True, null=True)
    is_confirm = models.BooleanField(verbose_name='是否确认肺动脉高压',
                                     choices=((False,'否'),(True,'是')),default=False,)
    why_not_confirm = models.CharField(verbose_name='未确诊原因', max_length=10,
                                       choices=(
                                           ("bqbyz","病情不严重"),
                                           ("jjyyzh","经济原因暂缓"),
                                           ("fcwhsyy","附近无合适医院"),
                                           ("other","其他（请注明）"),
                                       ),
                                       blank=True, null=True)
    # 确诊
    confirm_pah_date = models.DateField(verbose_name='确诊PAH日期',
                                        blank=True, null=True)
    confirm_hospital = models.CharField(verbose_name='确诊医院', max_length=20,
                                        blank=True, null=True)
    confirm_section = models.CharField(verbose_name='确诊科室', max_length=20,
                                       blank=True, null=True)
    confirm_doctor = models.CharField(verbose_name='医生', max_length=10,
                                      blank=True, null=True)
    exam_func = models.CharField(verbose_name='检查手段', max_length=20,
                                 choices=(
                                     ("xzcc","心脏彩超"),
                                     ("xdg","心导管"),
                                     ("fdmzy","肺动脉造影"),
                                     ("fzkt","肺阻抗图"),
                                     ("cgz","磁共振"),
                                     ("other","其他（请注明）"),
                                 ),
                                 blank=True, null=True)
    doctor_diagnosis = models.ImageField(verbose_name='医生诊断说明',
                                         help_text='上传诊断书照片，申请资助使用',
                                         upload_to='diagnosis',
                                         blank=True, null=True)
    incidence_reason = models.CharField(verbose_name='发病原因', max_length=100,
                                        choices=(
                                            ("tfx","特发性PAH"),
                                            ("jdzzbhb","结缔组织病合并PAH"),
                                            ("jzx","家族性PAH"),
                                            ("fss","肺栓塞"),
                                            ("xxfqhb","先心房缺合并PAH"),
                                            ("xxsqhb","先心室缺合并PAH"),
                                            ("fzxxhb","复杂先心合并PAH"),
                                            ("xxsh","先心术后PAH"),
                                            ("dmy","动脉炎"),
                                            ("bqc","不清楚病因或尚未明确诊断"),
                                            ("other","其他（请注明）"),
                                        ),
                                   blank=True, null=True)
    # 定期检查
    has_regular_check = models.BooleanField(verbose_name='是否定期检查',
                                            choices=((False,'否'),(True,'是')),default=False)
    regular_check_rate = models.PositiveIntegerField(verbose_name='定期检查频率',
                                                     choices=[(n, n) for n in range(1,13)].append((999,'其他')),
                                                     help_text='几个月进行一次检查',
                                   blank=True, null=True)
    un_regular_check_reason = models.CharField(verbose_name='不定期检查的原因',max_length=20,
                                               choices=(
                                                           ("bgwd","病情稳定"),
                                                           ("tmf","太麻烦"),
                                                           ("bzs","不重视"),
                                                           ("fytg","费用太高"),
                                                           ("ltyy","路途遥远"),
                                                           ("other","其他（请注明）"),
                                                       ),
                                               help_text='可多选',
                                   blank=True, null=True)
    # 日常
    routine_hospital = models.CharField(verbose_name='日常就诊医院', max_length=30,
                                        help_text='居住地附近的医院（外键）',
                                   blank=True, null=True)
    # 随访相关
    follow_up_hospital = models.CharField(verbose_name='随访检查医院', max_length=30,
                                          help_text='十大主要诊疗基地医院（外键）',
                                          blank=True, null=True)
    follow_up_doctor = models.CharField(verbose_name='随访主治医生', max_length=10,
                                        help_text='随访主治医生（外键）',
                                        blank=True, null=True)
    follow_up_target = models.CharField(verbose_name='随访检查目的', max_length=30,
                                        choices=(
                                            ("","波生坦赠药计划"),
                                            ("","安立生坦赠药计划"),
                                            ("","万他维赠药计划"),
                                            ("other","其他（请注明）"),
                                        ),
                                        blank=True, null=True)

    medical_evaluate = models.CharField(verbose_name='对医疗服务评价', max_length=20,
                                        choices=(
                                            ("fcmy","非常满意"),
                                            ("my","满意"),
                                            ("yb","一般"),
                                            ("bmy","不满意"),
                                            ("fcbmy","非常不满意"),
                                        ),
                                        blank=True, null=True)

    # 目前状况

    present_schedule = models.CharField(verbose_name='目前治疗方案', max_length=10,
                                   blank=True, null=True)
    present_schedule_pay = models.CharField(verbose_name='目前治疗方案每月药费', max_length=20,
                                   blank=True, null=True)
    present_drugs = models.CharField(verbose_name='目前用药(外键）', max_length=10,
                                   blank=True, null=True)
    other_drugs = models.CharField(verbose_name='上面没有列出的药物', max_length=30,
                                   blank=True, null=True)

    # 吸氧
    has_daily_oxygen = models.BooleanField(verbose_name='是否每天吸氧治疗',
                                           choices=((False,'否'),(True,'是')),default=False)
    daily_oxygen_hours = models.PositiveIntegerField(verbose_name='每天吸氧时间', help_text='单位：（小时）',
                                                     choices=[(n,n) for n in range(1,25)],
                                                     blank=True, null=True)
    oxygen_way = models.CharField(verbose_name='吸氧方式',max_length=10,
                                  choices=(
                                      ("jyzyj","家用制氧机"),
                                      ("yyzyj","医用制氧机"),
                                      ("yyhsq","医院或者社区医疗室"),
                                  ),
                                  blank=True, null=True)
    oxygenerator = models.CharField(verbose_name='制氧机品牌和型号', max_length=30,
                                    help_text="如：鱼跃 F-3000",
                                    blank=True, null=True)
    oxy_is_recommend = models.BooleanField(verbose_name='是否推荐此品牌',
                                           choices=((False,"不推荐"),(True,"推荐"),))

    # 经济状况
    year_drugs_pay = models.CharField(verbose_name='年药费支出', max_length=20,
                                        help_text="上述日常药物的费用，单位：元",
                                        blank=True, null=True)
    year_medical_pay = models.CharField(verbose_name='年治疗费支出', max_length=30,
                                        help_text='日常药费之外的住院、检查及差旅费',
                                        blank=True, null=True)

    year_pi = models.CharField(verbose_name='个人年收入', max_length=10,
                               blank=True, null=True)
    year_pi_source = models.CharField(verbose_name='个人收入来源', max_length=10,
                                      choices=(
                                          ("","工资收入"),
                                          ("","店铺公司经营利润"),
                                          ("","资金或房地产投资收益"),
                                          ("","劳务等服务收入"),
                                          ("other","其他（请注明）"),
                                      ),
                                      blank=True, null=True)
    year_home_income = models.CharField(verbose_name='家庭年收入', max_length=30,
                                        blank=True, null=True)
    debt = models.CharField(verbose_name='因病负债', max_length=10, help_text='治病借债金额，无则填0',
                            blank=True, null=True)

    medical_security =models.CharField(verbose_name='医疗保障情况', max_length=20,
                                       choices=(
                                           ("gfyl","公费医疗"),
                                           ("czjm","城镇居民"),
                                           ("czzg","城镇职工"),
                                           ("xnh","新农合"),
                                           ("cxyljz","城乡医疗救助"),
                                           ("mjhjb","民间罕见病医疗救助资金"),
                                           ("syyl","商业医疗保险"),
                                           ("myylbx","没有医疗保险"),
                                           ("other","其他（请注明）"),
                                       ),
                                       blank=True, null=True)

    medical_reimbur_ratio = models.CharField(verbose_name='医疗报销比例', max_length=20,
                                             blank=True, null=True)

    allowance = models.CharField(verbose_name='补助情况', max_length=10,
                                 choices=(
                                     ("db","低保"),
                                     ("cjrbzj","残疾人保障金"),
                                     ("dwcsjg","单位或慈善机构一次性补助"),
                                     ("dwylbx","单位医疗报销"),
                                     ("other","其他（请注明）"),
                                 ),
                                 blank=True, null=True)
    year_drugs_pay_by_self = models.CharField(verbose_name='年医药费自付金额',max_length=10,
                                              help_text='药费加治疗费减去补助和报销',
                                              blank=True, null=True)

    difficulty_in_treat = models.CharField(verbose_name='就诊过程中的困难', max_length=100,
                                           choices=(
                                               ("wzhlz","曾经被误诊或漏诊"),
                                               ("jjfqqz","因经济原因放弃确诊"),
                                               ("jjfqzl","因经济原因放弃正规治疗"),
                                               ("wfzz","无法办理转诊"),
                                               ("wfbx","可转诊但大部分费用无法报销"),
                                               ("other","其他苦难(请自述)"),
                                           ),
                                           blank=True, null=True)


    present_wish = models.TextField(verbose_name='目前的困难与期盼', max_length=500,
                                    help_text="列举主要心愿和期盼,不超过500字",
                                    blank=True, null=True)



    class Meta:
        verbose_name = '患者'
        permissions = (
            ('my_doctor', '患者医生可见'),
            ('my_hospital', '患者所在医院可见'),
        )


    def get_doctor(self):
        return self.doctorrecord_set.get(end_date=None, patient=self).doctor

    def get_url(self):

        return reverse('admin-detail-patient', kwargs={'pk': self.id})

    def __unicode__(self):

        return self.user.username

class Relative(models.Model):
    """ 患者亲人
    """

    patient = models.ForeignKey(Patient, verbose_name='病人',null=True,blank=True)

    relation = models.CharField(verbose_name='与病人关系', max_length=10,
                                choices=(
                                    ("papa","父亲"),
                                    ("mama","母亲"),
                                    ("boy","儿子"),
                                    ("girl","女儿"),
                                    ("lover","配偶"),
                                    ("other","其他"),
                                ))
    live_together = models.BooleanField(verbose_name='是否与病人共同生活', default=True)

    ## 外键 个人资料

    # 证明相关信息

    cert_username = models.CharField(verbose_name='证明人姓名', max_length=20,
                                     help_text='非直系或旁系亲属，与患者住在一起，可只需一名证明人;家在外地的，需不同证明人')
    cert_relation = models.CharField(verbose_name='与被证明人关系', max_length=30)
    cert_unit = models.CharField(verbose_name='证明人工作单位', max_length=50)
    cert_duty = models.CharField(verbose_name='证明人职务', max_length=50)
    cert_tele = models.CharField(verbose_name='证明人联系电话', max_length=15,
                                 help_text='申请资助时确认资料的真实性')


#class

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
























































