#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2019-04-27 00:11
"""


from libs.db_orm_id import DbInstance
from apps.databases.db_source import db
from apps.models.db_source.eap_user import EAPUser

db_instance = DbInstance(db)


def get_user_row_by_id(user_id):
    """
    通过 id 获取信息
    :param user_id:
    :return: None/object
    """
    return db_instance.get_row_by_id(EAPUser, user_id)


def get_user_row(*args, **kwargs):
    """
    获取信息
    :param args:
    :param kwargs:
    :return: None/object
    """
    return db_instance.get_row(EAPUser, *args, **kwargs)


def get_user_rows(*args, **kwargs):
    """
    获取列表
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_rows(EAPUser, *args, **kwargs)


def get_user_limit_rows_by_last_id(last_pk, limit_num, *args, **kwargs):
    """
    通过最后一个主键 id 获取最新信息列表
    :param last_pk:
    :param limit_num:
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.get_limit_rows_by_last_id(EAPUser, last_pk, limit_num, *args, **kwargs)


def add_user(user_data):
    """
    添加信息
    :param user_data:
    :return: None/Value of user.id
    :except:
    """
    return db_instance.add(EAPUser, user_data)


def edit_user(user_id, user_data):
    """
    修改信息
    :param user_id:
    :param user_data:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.edit(EAPUser, user_id, user_data)


def delete_user(user_id):
    """
    删除信息
    :param user_id:
    :return: Number of affected rows (Example: 0/1)
    :except:
    """
    return db_instance.delete(EAPUser, user_id)


def get_user_pagination(page=1, per_page=10, *args, **kwargs):
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
    rows = db_instance.get_pagination(EAPUser, page, per_page, *args, **kwargs)
    return rows


def delete_user_table():
    """
    清空表
    :return:
    """
    return db_instance.delete_table(EAPUser)


def count_user(*args, **kwargs):
    """
    计数
    :param args:
    :param kwargs:
    :return:
    """
    return db_instance.count(EAPUser, *args, **kwargs)
