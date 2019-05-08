#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2019-04-26 23:58
"""


from __future__ import unicode_literals

from flask_restful import fields

fields_item_user = {
    'id': fields.String(attribute='id'),
    'name': fields.String(attribute='Code'),
    'phone': fields.String(attribute='name'),
    'email': fields.String(attribute='email'),
}

fields_item_user_cn = {
    '主键': fields.String(attribute='id'),
    '姓名': fields.String(attribute='Code'),
    '手机': fields.String(attribute='name'),
    '邮箱': fields.String(attribute='email'),
}
