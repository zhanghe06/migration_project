#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-05-07 01:24
"""

from __future__ import unicode_literals

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
from apps.migrations.delivery.api import sync


class DeliveriesSyncResource(Resource):
    """
    DeliveriesSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/deliveries/sync
        :return:
        """
        return jsonify(sync())
