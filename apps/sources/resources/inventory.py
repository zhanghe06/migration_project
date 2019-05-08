#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: inventory.py
@time: 2019-04-27 14:58
"""

from __future__ import unicode_literals

from flask import jsonify, make_response
from flask_restful import Resource, marshal, reqparse

from apps import app
from apps.commons.exceptions import NotFound
from apps.commons.http_token_auth import token_auth
from apps.sources.apis.inventory import (
    get_inventory_row_by_id,
    delete_inventory,
    get_inventory_pagination)
from apps.sources.outputs.inventory import fields_item_inventory
from apps.sources.reqparsers.inventory import (
    structure_key_items,
    structure_key_item,
)

SUCCESS_MSG = app.config['SUCCESS_MSG']
FAILURE_MSG = app.config['FAILURE_MSG']


class InventoryResource(Resource):
    """
    InventoryResource
    """
    decorators = [token_auth.login_required]

    def get(self, pk):
        """
        Example:
            curl http://0.0.0.0:5000/source/inventory/1
        :param pk:
        :return:
        """
        data = get_inventory_row_by_id(pk)
        if not data:
            raise NotFound
        result = marshal(data, fields_item_inventory, envelope=structure_key_item)
        return jsonify(result)

    def delete(self, pk):
        """
        Example:
            curl http://0.0.0.0:5000/source/inventory/1 -X DELETE
        :param pk:
        :return:
        """
        result = delete_inventory(pk)
        if result:
            success_msg = SUCCESS_MSG.copy()
            return make_response(jsonify(success_msg), 204)
        else:
            failure_msg = FAILURE_MSG.copy()
            return make_response(jsonify(failure_msg), 400)


class InventoriesResource(Resource):
    """
    InventoriesResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/source/inventories
            curl http://0.0.0.0:5000/source/inventories?page=1&per_page=20
        :return:
        """
        # 条件参数
        filter_parser = reqparse.RequestParser(bundle_errors=True)
        filter_parser.add_argument('page', type=int, default=1, location='args')
        filter_parser.add_argument('per_page', type=int, default=20, location='args')

        filter_parser_args = filter_parser.parse_args()

        pagination_obj = get_inventory_pagination(**filter_parser_args)

        result = marshal(pagination_obj.items, fields_item_inventory, envelope=structure_key_items)
        result['total'] = pagination_obj.total
        return jsonify(result)
