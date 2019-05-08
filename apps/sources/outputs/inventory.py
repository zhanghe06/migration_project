#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: inventory.py
@time: 2019-04-26 14:23
"""


from __future__ import unicode_literals

from flask_restful import fields


fields_item_inventory = {
    'id': fields.String(attribute='id'),
    'code': fields.String(attribute='code'),  # 编码
    'name': fields.String(attribute='name'),  # 名称
    'specification': fields.String(attribute='specification'),  # 规格
    'invs_cost': fields.Float(attribute='invSCost'),  # 参考成本
    'latest_cost': fields.Float(attribute='latestCost'),  # 最新成本
    'avag_cost': fields.Float(attribute='avagCost'),  # 平均成本
    'warehouse_id': fields.String(attribute='idwarehouse'),  # 仓库id
    'warehouse_name': fields.String(attribute='warehouse_name'),  # 仓库名称
    'brand_id': fields.String(attribute='productInfo'),  # 品牌id
    'brand_name': fields.String(attribute='brand_name'),  # 品牌名称
    'create_time': fields.String(attribute='createdTime'),
    'update_time': fields.String(attribute='updated'),
    # 'create_time': fields.DateTime(dt_format=b'iso8601', attribute='createdTime'),
    # 'update_time': fields.DateTime(dt_format=b'iso8601', attribute='updated'),
}

fields_item_inventory_cn = {
    '主键': fields.String(attribute='id'),
    '编码': fields.String(attribute='code'),  # 编码
    '名称': fields.String(attribute='name'),  # 名称
    '规格': fields.String(attribute='specification'),  # 规格
    '参考成本': fields.Float(attribute='invSCost'),  # 参考成本
    '最新成本': fields.Float(attribute='latestCost'),  # 最新成本
    '平均成本': fields.Float(attribute='avagCost'),  # 平均成本
    '仓库id': fields.String(attribute='idwarehouse'),  # 仓库id
    '仓库名称': fields.String(attribute='warehouse_name'),  # 仓库名称
    '品牌id': fields.String(attribute='productInfo'),  # 品牌id
    '品牌名称': fields.String(attribute='brand_name'),  # 品牌名称
    '创建时间': fields.String(attribute='createdTime'),
    '更细时间': fields.String(attribute='updated'),
    # '创建时间': fields.DateTime(dt_format=b'iso8601', attribute='createdTime'),
    # '更细时间': fields.DateTime(dt_format=b'iso8601', attribute='updated'),
}
