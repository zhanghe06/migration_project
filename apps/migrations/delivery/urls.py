#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-05-07 01:24
"""


from apps.migrations import migrations_api
from apps.migrations.delivery.resource import (
    DeliveriesSyncResource,
)

# 销货
migrations_api.add_resource(
    DeliveriesSyncResource,
    '/deliveries/sync',
    endpoint='deliveries_sync',
    strict_slashes=False
)
