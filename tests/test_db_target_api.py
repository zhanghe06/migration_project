#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_db_target_api.py
@time: 2019-09-05 15:20
"""


from libs.db_orm_api import DbApi

from apps.models.db_target import User
from apps.databases.db_target import get_target_db, target_db


# 测试开启以下配置
# SQLALCHEMY_ECHO = True


def test01():
    """共用连接"""
    print(test01.__doc__)
    target_user_api = DbApi(target_db, User)
    print(target_user_api.count())
    target_user_api = DbApi(target_db, User)
    print(target_user_api.count())


def test02():
    """共用连接"""
    print(test02.__doc__)
    print(DbApi(target_db, User).count())
    print(DbApi(target_db, User).count())


def test03():
    """独立连接"""
    print(test03.__doc__)
    target_user_api = DbApi(get_target_db(), User)
    print(target_user_api.count())
    target_user_api = DbApi(get_target_db(), User)
    print(target_user_api.count())


def test04():
    """独立连接"""
    print(test04.__doc__)
    print(DbApi(get_target_db(), User).count())
    print(DbApi(get_target_db(), User).count())


if __name__ == '__main__':
    test01()
    test02()
    test03()
    test04()
