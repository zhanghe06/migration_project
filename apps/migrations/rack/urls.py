#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-05-05 17:30
"""

from apps.migrations import migrations_api
from apps.migrations.rack.resource import (
    RacksSyncResource,
)

# 货位
migrations_api.add_resource(
    RacksSyncResource,
    '/racks/sync',
    endpoint='racks_sync',
    strict_slashes=False
)
