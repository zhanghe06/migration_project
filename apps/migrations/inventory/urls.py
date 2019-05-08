#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-05-06 19:07
"""


from apps.migrations import migrations_api
from apps.migrations.inventory.resource import (
    InventoriesSyncResource,
)

# 存货
migrations_api.add_resource(
    InventoriesSyncResource,
    '/inventories/sync',
    endpoint='inventories_sync',
    strict_slashes=False
)
