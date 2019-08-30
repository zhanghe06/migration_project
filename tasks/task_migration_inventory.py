#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: task_migration_inventory.py
@time: 2019-05-31 15:43
"""

from __future__ import print_function
from __future__ import unicode_literals

from apps.migrations.inventory.api import sync
from tools.decorator import log_api_exception_with_desc


@log_api_exception_with_desc('库存信息同步')
def migration_inventory():
    sync()


if __name__ == '__main__':
    migration_inventory()
