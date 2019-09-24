#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: user.py
@time: 2019-04-26 23:58
"""


from __future__ import unicode_literals

from datetime import datetime

from flask import jsonify, make_response
from flask_restful import Resource, marshal, reqparse

from apps.sources.outputs.user import fields_item_user, fields_item_user_cn
from apps.sources.reqparsers.user import (
    structure_key_item,
    structure_key_items,
    structure_key_item_cn,
    structure_key_items_cn,
)
from apps.models.db_source.eap_user import EAPUser
from apps.commons.exceptions import BadRequest, NotFound
from apps.sources.apis.user import (
    get_user_pagination)
from apps.commons.http_token_auth import token_auth
from apps import app

SUCCESS_MSG = app.config['SUCCESS_MSG']
FAILURE_MSG = app.config['FAILURE_MSG']


class UsersResource(Resource):
    """
    UsersResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/sources/users
            curl http://0.0.0.0:5000/sources/users?page=1&per_page=20
        :return:
        """
        # 条件参数
        filter_parser = reqparse.RequestParser(bundle_errors=True)
        filter_parser.add_argument('page', type=int, default=1, location='args')
        filter_parser.add_argument('per_page', type=int, default=20, location='args')

        filter_parser_args = filter_parser.parse_args()

        pagination_obj = get_user_pagination(**filter_parser_args)

        result = marshal(pagination_obj.items, fields_item_user, envelope=structure_key_items)
        result['total'] = pagination_obj.total
        return jsonify(result)
