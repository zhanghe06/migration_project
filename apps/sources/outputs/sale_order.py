#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: sale_order.py
@time: 2019-04-26 16:59
"""


from __future__ import unicode_literals

from flask_restful import fields

fields_item_sale_order = {
    'id': fields.Integer(attribute='ID'),
    'code': fields.String(attribute='code'),
    'customer_id': fields.Integer(attribute='idcustomer'),  # 客户id
    'settle_id': fields.Integer(attribute='idsettlecustomer'),  # 结算客户id
    'address': fields.String(attribute='address'),
    'linkman': fields.String(attribute='linkMan'),
    'amount': fields.Float(attribute='amount'),
    'amount_tax': fields.Float(attribute='taxAmount'),
    'contact_phone': fields.String(attribute='contactPhone'),
    'delivery_mode': fields.Integer(attribute='deliveryMode'),
    'receive_type': fields.Integer(attribute='reciveType'),
    'maker_id': fields.Integer(attribute='makerid'),
    'maker': fields.String(attribute='maker'),
    'create_time': fields.DateTime(dt_format=b'iso8601', attribute='createdtime'),
    'update_time': fields.DateTime(dt_format=b'iso8601', attribute='updated'),
}

fields_item_sale_order_cn = {
    '主键': fields.Integer(attribute='ID'),
    '编号': fields.String(attribute='code'),
    '客户': fields.Integer(attribute='idcustomer'),  # 客户id
    '结算单位': fields.Integer(attribute='idsettlecustomer'),  # 结算客户id
    '地址': fields.String(attribute='address'),
    '联系人': fields.String(attribute='linkMan'),
    '金额': fields.Float(attribute='amount'),
    '含税金额': fields.Float(attribute='taxAmount'),
    '联系电话': fields.String(attribute='contactPhone'),
    '运输方式': fields.Integer(attribute='deliveryMode'),
    '收款方式': fields.Integer(attribute='reciveType'),
    '制单人ID': fields.Integer(attribute='makerid'),
    '制单人': fields.String(attribute='maker'),
    '创建时间': fields.DateTime(dt_format=b'iso8601', attribute='createdtime'),
    '更细时间': fields.DateTime(dt_format=b'iso8601', attribute='updated'),
}
