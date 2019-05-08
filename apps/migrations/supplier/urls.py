#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-04-27 23:54
"""


from apps.migrations import migrations_api
from apps.migrations.supplier.resource import (
    SuppliersSyncResource,
)

# 友商
migrations_api.add_resource(
    SuppliersSyncResource,
    '/suppliers/sync',
    endpoint='suppliers_sync',
    strict_slashes=False
)
