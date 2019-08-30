#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: task_migration_user.py
@time: 2019-08-30 10:24
"""

from __future__ import print_function
from __future__ import unicode_literals

from apps.migrations.user.api import sync
from tools.decorator import log_api_exception_with_desc


@log_api_exception_with_desc('用户信息同步')
def migration_user():
    sync()


if __name__ == '__main__':
    migration_user()
