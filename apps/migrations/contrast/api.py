#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2019-05-06 15:52
"""

import datetime

from apps.databases.db_migration import db
from apps.models.db_migration import Contrast
from libs.db_orm_pk import DbInstance

db_instance = DbInstance(db)


def get_contrast_row_by_id(contrast_id):
    """
    通过 id 获取信息
    :param contrast_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(Contrast, contrast_id)


def get_contrast_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(Contrast, *args, **kwargs)


def get_contrast_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(Contrast, *args, **kwargs)


def get_contrast_limit_rows_by_last_id(last_pk, limit_num, *args, **kwargs):
    """
    通过最后一个主键 id 获取最新信息列表
    :param last_pk:
    :param limit_num:
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_limit_rows_by_last_id(Contrast, last_pk, limit_num, *args, **kwargs)


def add_contrast(contrast_data):
    """
    添加信息
    :param contrast_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(Contrast, contrast_data)


def edit_contrast(contrast_id, contrast_data):
    """
    修改信息
    :param contrast_id:
    :param contrast_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(Contrast, contrast_id, contrast_data)


def delete_contrast(contrast_id, force=False):
    """
    删除信息
    :param contrast_id:
    :param force:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    if force:
        return db_instance.delete(Contrast, contrast_id)
    else:
        data = {
            'status_delete': True,
            'delete_time': datetime.datetime.utcnow()
        }
        return db_instance.edit(Contrast, contrast_id, data)


def get_contrast_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(Contrast, page, per_page, *args, **kwargs)
    return rows


def delete_contrast_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(Contrast)


def count_contrast(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(Contrast, *args, **kwargs)
