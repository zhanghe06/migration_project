#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_db_source_api.py
@time: 2019-09-05 15:20
"""


from libs.db_orm_api import DbApi

from apps.models.db_source.eap_user import EAPUser
from apps.databases.db_source import get_source_db, source_db


# 测试开启以下配置
# SQLALCHEMY_ECHO = True


def test01():
    """共用连接"""
    print(test01.__doc__)
    source_user_api = DbApi(source_db, EAPUser)
    print(source_user_api.count())
    source_user_api = DbApi(source_db, EAPUser)
    print(source_user_api.count())


def test02():
    """独立连接"""
    print(test02.__doc__)
    source_user_api = DbApi(get_source_db(), EAPUser)
    print(source_user_api.count())
    source_user_api = DbApi(get_source_db(), EAPUser)
    print(source_user_api.count())


if __name__ == '__main__':
    test01()
    test02()
