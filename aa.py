#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhwei'

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pahchina.settings")
sys.path.append('./')

import json
import pahchina.settings


from pahchina.apps.region.models import Region
#from pahchina.apps.accounts.models import User
#print User.objects.all()

#Region.objects.create(name=n, patient=p)

with open('city.min.js') as fi:
    j = json.load(fi)

for jj in j['citylist']:
    print jj['p']
    p = Region.objects.create(name=jj['p'])
    try:
        for i in  jj['c']:
            #print i['n']
            Region.objects.create(name=i['n'], parent=p)
    except KeyError:
        print 'no city'