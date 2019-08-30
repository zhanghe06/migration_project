#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-05-08 16:32
"""

from apps.migrations import migrations_api
from apps.migrations.purchase.resource import (
    PurchasesSyncResource,
)

# 进货
migrations_api.add_resource(
    PurchasesSyncResource,
    '/purchases/sync',
    endpoint='purchases_sync',
    strict_slashes=False
)
