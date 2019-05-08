#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enum.py
@time: 2019-04-26 15:09
"""


from apps.sources import sources_api
from apps.sources.resources.enum import (
    EnumResource,
    EnumsResource,
)

# 枚举类型
sources_api.add_resource(
    EnumResource,
    '/enum/<int:pk>',
    endpoint='enum',
    strict_slashes=False
)

sources_api.add_resource(
    EnumsResource,
    '/enums',
    endpoint='enums',
    strict_slashes=False
)
