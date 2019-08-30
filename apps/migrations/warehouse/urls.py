#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-05-05 17:30
"""

from apps.migrations import migrations_api
from apps.migrations.warehouse.resource import (
    WarehousesSyncResource,
)

# 仓库
migrations_api.add_resource(
    WarehousesSyncResource,
    '/warehouses/sync',
    endpoint='warehouses_sync',
    strict_slashes=False
)
