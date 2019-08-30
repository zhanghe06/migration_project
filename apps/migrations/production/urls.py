#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-04-27 16:31
"""

from apps.migrations import migrations_api
from apps.migrations.production.resource import (
    ProductionsSyncResource,
)

# 产品
migrations_api.add_resource(
    ProductionsSyncResource,
    '/productions/sync',
    endpoint='productions_sync',
    strict_slashes=False
)
