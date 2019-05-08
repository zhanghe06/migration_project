#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enum_items.py
@time: 2019-04-26 15:55
"""


from __future__ import unicode_literals

from flask_restful import fields

fields_item_enum_items = {
    'id': fields.String(attribute='id'),
    'id_enum': fields.String(attribute='idEnum'),
    'code': fields.String(attribute='Code'),
    'name': fields.String(attribute='Name'),
    'is_deleted': fields.Boolean(attribute='IsDeleted'),
}

fields_item_enum_items_cn = {
    '主键': fields.String(attribute='id'),
    '枚举id': fields.String(attribute='idEnum'),
    '编码': fields.String(attribute='Code'),
    '名称': fields.String(attribute='Name'),
    '删除': fields.Boolean(attribute='IsDeleted'),
}
