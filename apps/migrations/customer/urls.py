#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-04-27 23:33
"""


from apps.migrations import migrations_api
from apps.migrations.customer.resource import (
    CustomersSyncResource,
)

# 客户
migrations_api.add_resource(
    CustomersSyncResource,
    '/customers/sync',
    endpoint='customers_sync',
    strict_slashes=False
)
