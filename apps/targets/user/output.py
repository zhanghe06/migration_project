#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: output.py
@time: 2019-05-30 01:32
"""


from __future__ import unicode_literals

from flask_restful import fields

fields_item_user = {
    'id': fields.String(attribute='id'),
    'name': fields.String(attribute='name'),
    'salutation': fields.String(attribute='salutation'),
    'mobile': fields.String(attribute='mobile'),
    'tel': fields.String(attribute='tel'),
    'fax': fields.String(attribute='fax'),
    'email': fields.String(attribute='email'),
    'create_time': fields.DateTime(dt_format=b'iso8601'),
    'update_time': fields.DateTime(dt_format=b'iso8601'),
}

fields_item_user_cn = {
    '主键': fields.String(attribute='id'),
    'name': fields.String(attribute='name'),
    'salutation': fields.String(attribute='salutation'),
    'mobile': fields.String(attribute='mobile'),
    'tel': fields.String(attribute='tel'),
    'fax': fields.String(attribute='fax'),
    'email': fields.String(attribute='email'),
    'create_time': fields.DateTime(dt_format=b'iso8601'),
    'update_time': fields.DateTime(dt_format=b'iso8601'),
}
