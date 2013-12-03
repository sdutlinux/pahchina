#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from ...apps.utils.models import TimeStampedModel
from ...apps.accounts.models import User

# Create your models here.
class News(TimeStampedModel):
    title = models.CharField()
    content = models.TextField()
    author = models.ForeignKey(User)
    site = models.ManyToManyField()
    