#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_sqlalchemy_failure.py
@time: 2019-09-04 16:20
"""

import time

# from flask_sqlalchemy import SQLAlchemy
#
# from apps import app
# from apps.models.db_target import User
# from libs.db_orm_pk import DbInstance
from apps.targets.user.api import get_user_rows

# db = SQLAlchemy(app)


def test():
    i = 0
    # for user in DbInstance(db).get_rows(User):
    for user in get_user_rows():
        if i > 5:
            break
        print(user.name)
        time.sleep(1)
        i += 1


if __name__ == '__main__':
    test()
    test()

"""
SQLALCHEMY_POOL_RECYCLE = 5
SQLALCHEMY_ECHO = True

SET GLOBAL wait_timeout=5;

python tests/test_sqlalchemy_failure.py
"""
