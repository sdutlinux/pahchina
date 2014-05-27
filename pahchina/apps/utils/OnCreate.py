#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

from django.db.models.signals import post_save

from ..accounts.models import User
from ..patient.models import Patient
from ..volunteer.models import Volunteer
from ..medical.models import Hospital, Doctor, DoctorRecord



def on_create(sender, instance, created, **kwargs):
    """ 创建用户的时候同步创建其他类型的用户
    """
    if created:
        print instance.is_patient
        if instance.is_patient:
            Patient.objects.create(user=instance)
        elif instance.is_volunteer:
            Volunteer.objects.create(user=instance)
        elif instance.is_hospital:
            Hospital.objects.create(user=instance)
        elif instance.is_doctor:
            Doctor.objects.create(user=instance)
        else:
            pass


#def patient_doctor_record(sender, instance, created, **kwargs):
#
#    if created:
#        if instance.end_date is None:
#            Patient.objects.get(id=instance.patient.id).update(doctor=instance.doctor)
#        else:
#            pass

# post_save.connect(on_create, sender=User, weak=False,
#           dispatch_uid='models.on_create')
#post_save.connect(patient_doctor_record, sender=DoctorRecord, weak=False,
#          dispatch_uid='models.patient_doctor_record')