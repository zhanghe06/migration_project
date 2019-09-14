#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_sqlalchemy_close.py
@time: 2019-09-07 17:24
"""

import time

from libs.db_orm_api import DbApi

from apps.models.db_target import User
from apps.databases.db_target import get_target_db


# 测试开启以下配置
# SQLALCHEMY_ECHO = True


def test01():
    """不关连接"""
    print(test01.__doc__)
    target_user_api = DbApi(get_target_db(), User)
    users = target_user_api.get_rows()
    for user in users:
        time.sleep(1)
        print(user.name)
        break
    target_user_api = DbApi(get_target_db(), User)
    users = target_user_api.get_rows()
    for user in users:
        time.sleep(1)
        print(user.name)
        break


def test02():
    """关闭连接"""
    print(test02.__doc__)
    target_user_api = DbApi(get_target_db(), User)
    users = target_user_api.get_rows()

    for user in users:
        time.sleep(1)
        print(user.name)


if __name__ == '__main__':
    test01()
    # test02()
