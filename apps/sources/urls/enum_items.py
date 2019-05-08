#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enum_items.py
@time: 2019-04-26 15:10
"""


from apps.sources import sources_api
from apps.sources.resources.enum_items import (
    EnumItemResource,
    EnumItemsResource,
)

# 枚举类型明细
sources_api.add_resource(
    EnumItemResource,
    '/enum_item/<int:pk>',
    endpoint='enum_item',
    strict_slashes=False
)

sources_api.add_resource(
    EnumItemsResource,
    '/enum_items',
    endpoint='enum_items',
    strict_slashes=False
)
