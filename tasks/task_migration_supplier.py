#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: task_migration_supplier.py
@time: 2019-05-31 15:43
"""

from __future__ import print_function
from __future__ import unicode_literals

from apps.migrations.supplier.api import sync
from tools.decorator import log_api_exception_with_desc


@log_api_exception_with_desc('友商信息同步')
def migration_supplier():
    return sync()


if __name__ == '__main__':
    migration_supplier()
