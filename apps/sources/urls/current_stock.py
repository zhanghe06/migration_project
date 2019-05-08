#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: current_stock.py
@time: 2019-04-26 15:09
"""


from apps.sources import sources_api
from apps.sources.resources.current_stock import (
    CurrentStockResource,
    CurrentStocksResource,
)

# 当前库存
sources_api.add_resource(
    CurrentStockResource,
    '/current_stock/<int:pk>',
    endpoint='current_stock',
    strict_slashes=False
)

sources_api.add_resource(
    CurrentStocksResource,
    '/current_stocks',
    endpoint='current_stocks',
    strict_slashes=False
)
