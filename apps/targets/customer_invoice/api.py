#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2019-04-27 16:38
"""


import datetime

from libs.db_orm_pk import DbInstance
from apps.databases.db_target import db
from apps.models.db_target import CustomerInvoice

db_instance = DbInstance(db)


def get_customer_invoice_row_by_id(customer_invoice_id):
    """
    通过 id 获取信息
    :param customer_invoice_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(CustomerInvoice, customer_invoice_id)


def get_customer_invoice_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(CustomerInvoice, *args, **kwargs)


def get_customer_invoice_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(CustomerInvoice, *args, **kwargs)


def get_customer_invoice_limit_rows_by_last_id(last_pk, limit_num, *args, **kwargs):
    """
    通过最后一个主键 id 获取最新信息列表
    :param last_pk:
    :param limit_num:
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_limit_rows_by_last_id(CustomerInvoice, last_pk, limit_num, *args, **kwargs)


def add_customer_invoice(customer_invoice_data):
    """
    添加信息
    :param customer_invoice_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(CustomerInvoice, customer_invoice_data)


def edit_customer_invoice(customer_invoice_id, customer_invoice_data):
    """
    修改信息
    :param customer_invoice_id:
    :param customer_invoice_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(CustomerInvoice, customer_invoice_id, customer_invoice_data)


def delete_customer_invoice(customer_invoice_id, force=False):
    """
    删除信息
    :param customer_invoice_id:
    :param force:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    if force:
        return db_instance.delete(CustomerInvoice, customer_invoice_id)
    else:
        data = {
            'status_delete': True,
            'delete_time': datetime.datetime.utcnow()
        }
        return db_instance.edit(CustomerInvoice, customer_invoice_id, data)


def get_customer_invoice_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(CustomerInvoice, page, per_page, *args, **kwargs)
    return rows


def delete_customer_invoice_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(CustomerInvoice)


def count_customer_invoice(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(CustomerInvoice, *args, **kwargs)

