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
text = """
    {
        "pk": {0},
        "model": "region.Region",
        "fields": {
            "name": "{1}",
            "parent": "{2}",
        }
    },
"""

def w_json(id, name, parent=''):
    #f_name = 'test.json'
    with open('pahchina/backup/test.json','a') as fi:
        text = \
"""    {
        "pk": %s,
        "model": "region.Region",
        "fields": {
            "name": "%s",
            "parent": %s
        }
    },""" % (id, name, parent)
        #print type(text)
        fi.write(text.encode('utf-8'))
        fi.write('\n')


with open('pahchina/backup/city.min.js') as fi:
    province_list = json.load(fi)

for province in province_list:
    print province['n']
    p = Region.objects.create(name=province['n'])
    try:
        for city in  province['s']:
            print city['n']
            c = Region.objects.create(name=city['n'], parent=p)
            try:
                for area in city['s']:
                    print area['n']
                    a = Region.objects.create(name=area['n'], parent=c)
            except KeyError:
                print 'no area'
    except KeyError:
        print 'no city'