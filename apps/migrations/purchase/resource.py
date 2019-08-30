#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-05-08 16:32
"""

from __future__ import unicode_literals

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
# from apps.sources.apis.current_stock import (
#     get_current_stock_row_by_id as sources_get_purchase_row_by_id,
#     get_current_stock_limit_rows_by_last_id as sources_get_purchase_limit_rows_by_last_id,
#     count_current_stock as sources_count_purchase,
# )
from apps.migrations.purchase.api import sync


class PurchasesSyncResource(Resource):
    """
    PurchasesSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/purchases/sync
        :return:
        """

        return jsonify(sync())
