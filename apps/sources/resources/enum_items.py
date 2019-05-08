#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: enum_items_items.py
@time: 2019-04-27 15:56
"""


from __future__ import unicode_literals

from flask import jsonify, make_response
from flask_restful import Resource, marshal, reqparse, inputs

from apps.sources.outputs.enum_items import fields_item_enum_items, fields_item_enum_items_cn
from apps.sources.reqparsers.enum_items import (
    structure_key_item,
    structure_key_items,
    structure_key_item_cn,
    structure_key_items_cn,
)

from apps.commons.exceptions import BadRequest, NotFound
from apps.sources.apis.enum_items import (
    get_enum_items_row_by_id,
    edit_enum_items,
    delete_enum_items,
    get_enum_items_limit_rows_by_last_id,
    add_enum_items,
    get_enum_items_pagination,
)
from apps.commons.http_token_auth import token_auth
from apps import app

SUCCESS_MSG = app.config['SUCCESS_MSG']
FAILURE_MSG = app.config['FAILURE_MSG']


class EnumItemResource(Resource):
    """
    EnumItemResource
    """
    decorators = [token_auth.login_required]

    def get(self, pk):
        """
        Example:
            curl http://0.0.0.0:5000/sources/enum_item/1
        :param pk:
        :return:
        """
        data = get_enum_items_row_by_id(pk)
        if not data:
            raise NotFound
        result = marshal(data, fields_item_enum_items_cn, envelope=structure_key_item_cn)
        return jsonify(result)

    def delete(self, pk):
        """
        Example:
            curl http://0.0.0.0:5000/sources/enum_item/1 -X DELETE
        :param pk:
        :return:
        """
        result = delete_enum_items(pk)
        if result:
            success_msg = SUCCESS_MSG.copy()
            return make_response(jsonify(success_msg), 204)
        else:
            failure_msg = FAILURE_MSG.copy()
            return make_response(jsonify(failure_msg), 400)


class EnumItemsResource(Resource):
    """
    EnumItemsResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/sources/enum_items/pagination
            curl http://0.0.0.0:5000/sources/enum_items/pagination?page=2000&per_page=2
        :return:
        """
        # 条件参数
        filter_parser = reqparse.RequestParser(bundle_errors=True)
        filter_parser.add_argument('page', type=int, default=1, location='args')
        filter_parser.add_argument('per_page', type=int, default=20, location='args')

        filter_parser.add_argument('id_enum', location='args', dest='idEnum', store_missing=False)
        filter_parser.add_argument('name', location='args', dest='Name', store_missing=False)
        filter_parser.add_argument('is_deleted', type=inputs.boolean, location='args', dest='IsDeleted',
                                   store_missing=False)

        filter_parser_args = filter_parser.parse_args()

        pagination_obj = get_enum_items_pagination(**filter_parser_args)

        result = marshal(pagination_obj.items, fields_item_enum_items, envelope=structure_key_items)
        result['total'] = pagination_obj.total
        return jsonify(result)
