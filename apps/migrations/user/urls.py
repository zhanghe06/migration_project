#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-05-06 17:26
"""


from apps.migrations import migrations_api
from apps.migrations.user.resource import (
    UsersSyncResource,
)

# 用户
migrations_api.add_resource(
    UsersSyncResource,
    '/users/sync',
    endpoint='users_sync',
    strict_slashes=False
)
