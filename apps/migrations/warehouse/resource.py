#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-05-05 17:30
"""

from __future__ import unicode_literals

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
from apps.migrations.warehouse.api import sync


class WarehousesSyncResource(Resource):
    """
    WarehousesSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/warehouses/sync
        :return:
        """

        return jsonify(sync())
