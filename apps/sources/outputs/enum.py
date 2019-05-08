#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enum.py
@time: 2019-04-26 15:55
"""


from __future__ import unicode_literals

from flask_restful import fields

fields_item_enum = {
    'id': fields.String(attribute='id'),
    'name': fields.String(attribute='Name'),
    'title': fields.String(attribute='Title'),
}

fields_item_enum_cn = {
    '主键': fields.String(attribute='id'),
    '名称': fields.String(attribute='Name'),
    '标题': fields.String(attribute='Title'),
}
