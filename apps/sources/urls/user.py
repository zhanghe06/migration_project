#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2019-04-27 00:15
"""


from apps.sources import sources_api
from apps.sources.resources.user import (
    UsersResource,
)

# 用户
sources_api.add_resource(
    UsersResource,
    '/users',
    endpoint='users',
    strict_slashes=False
)
