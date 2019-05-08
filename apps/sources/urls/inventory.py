#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: inventory.py
@time: 2019-04-26 15:10
"""


from apps.sources import sources_api
from apps.sources.resources.inventory import (
    InventoryResource,
    InventoriesResource,
)

# 存货
sources_api.add_resource(
    InventoryResource,
    '/inventory/<int:pk>',
    endpoint='inventory',
    strict_slashes=False
)

sources_api.add_resource(
    InventoriesResource,
    '/inventories',
    endpoint='inventories',
    strict_slashes=False
)
