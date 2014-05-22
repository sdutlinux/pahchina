#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..region.models import LivingRegion

def get_my_users(website):
    """ 通过站点获取它的用户列表
    """
    def get_province_list():
        region_list = website.region_set.all()
        for r in region_list:
            yield r.name

    for p in get_province_list():
        for l in LivingRegion.objects.filter(cate='juzhu', province=p):
            yield l.user