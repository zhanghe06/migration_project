#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: current_stock.py
@time: 2019-04-26 14:23
"""


from __future__ import unicode_literals

from flask_restful import fields


fields_item_current_stock = {
    'id': fields.String(attribute='id'),
    'batch': fields.String(attribute='batch'),  # 批次
    'base_quantity': fields.Integer(attribute='baseQuantity'),  # 数量
    'id_inventory': fields.String(attribute='idinventory'),  # 产品id
    'id_baseunit': fields.String(attribute='idbaseunit'),  # 单位id
    'id_warehouse': fields.String(attribute='idwarehouse'),  # 仓库id
    'create_time': fields.String(attribute='createdtime'),
    'update_time': fields.String(attribute='updated'),
    # 'create_time': fields.DateTime(dt_format=b'iso8601', attribute='createdtime'),
    # 'update_time': fields.DateTime(dt_format=b'iso8601', attribute='updated'),
}

fields_item_current_stock_cn = {
    '主键': fields.String(attribute='id'),
    '批次': fields.String(attribute='batch'),  # 批次
    '数量': fields.Integer(attribute='baseQuantity'),  # 数量
    '产品': fields.String(attribute='idinventory'),  # 产品id
    '单位': fields.String(attribute='idbaseunit'),  # 单位id
    '仓库': fields.String(attribute='idwarehouse'),  # 仓库id
    '创建时间': fields.String(attribute='createdtime'),
    '更细时间': fields.String(attribute='updated'),
    # '创建时间': fields.DateTime(dt_format=b'iso8601', attribute='createdtime'),
    # '更细时间': fields.DateTime(dt_format=b'iso8601', attribute='updated'),
}
