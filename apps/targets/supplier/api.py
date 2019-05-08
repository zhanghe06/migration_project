#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2019-04-27 23:38
"""


import datetime

from libs.db_orm_pk import DbInstance
from apps.databases.db_target import db
from apps.models.db_target import Supplier

from apps.targets.supplier_contact.api import get_supplier_contact_rows
from apps.targets.supplier_invoice.api import get_supplier_invoice_row_by_id


db_instance = DbInstance(db)


def get_supplier_row_by_id(supplier_id):
    """
    通过 id 获取信息
    :param supplier_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Supplier, supplier_id)


def get_supplier_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Supplier, *args, **kwargs)


def get_supplier_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Supplier, *args, **kwargs)


def get_supplier_limit_rows_by_last_id(last_pk, limit_num, *args, **kwargs):
    """
    通过最后一个主键 id 获取最新信息列表
    :param last_pk:
    :param limit_num:
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_limit_rows_by_last_id(Supplier, last_pk, limit_num, *args, **kwargs)


def add_supplier(supplier_data):
    """
    添加信息
    :param supplier_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Supplier, supplier_data)


def edit_supplier(supplier_id, supplier_data):
    """
    修改信息
    :param supplier_id:
    :param supplier_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Supplier, supplier_id, supplier_data)


def delete_supplier(supplier_id, force=False):
    """
    删除信息
    :param supplier_id:
    :param force:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    if force:
        return db_instance.delete(Supplier, supplier_id)
    else:
        data = {
            'status_delete': True,
            'delete_time': datetime.datetime.utcnow()
        }
        return db_instance.edit(Supplier, supplier_id, data)


def get_supplier_pagination(page=1, per_page=10, *args, **kwargs):
    """
    获取列表（分页）
    Usage:
        items: 信息列表
        has_next: 如果本页之后还有超过一个分页，则返回True
        has_prev: 如果本页之前还有超过一个分页，则返回True
        next_num: 返回下一页的页码
        prev_num: 返回上一页的页码
        iter_pages(): 页码列表
        iter_pages(left_edge=2, left_current=2, right_current=5, right_edge=2) 页码列表默认参数
    :param page:
    :param per_page:
    :param args:
    :param kwargs:
    :return:
    """
    rows = db_instance.get_pagination(Supplier, page, per_page, *args, **kwargs)
    return rows


def delete_supplier_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(Supplier)


def count_supplier(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(Supplier, *args, **kwargs)


def get_supplier_detail_info(supplier_id):
    """
    获取详情
    :param supplier_id:
    :return: None/object
    """
    # 渠道详情
    supplier_info = db_instance.get_row_by_id(Supplier, supplier_id)

    if not supplier_info:
        return None

    # 联系方式
    supplier_contact_list = get_supplier_contact_rows(cid=supplier_id)
    supplier_info.supplier_contacts = supplier_contact_list

    # 开票资料
    supplier_invoice = get_supplier_invoice_row_by_id(supplier_id)
    supplier_info.supplier_invoice = supplier_invoice

    return supplier_info
