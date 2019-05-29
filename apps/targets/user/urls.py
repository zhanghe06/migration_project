#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-05-30 01:35
"""


from apps.targets import targets_api
from apps.targets.user.resource import (
    UsersResource,
)

# 用户
targets_api.add_resource(
    UsersResource,
    '/users',
    endpoint='users',
    strict_slashes=False
)

