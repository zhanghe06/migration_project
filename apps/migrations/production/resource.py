#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-04-27 16:31
"""


from __future__ import unicode_literals

from datetime import datetime

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
from apps.migrations.contrast.api import add_contrast
from apps.sources.apis.enum_items import get_enum_items_row_by_id
from apps.sources.apis.inventory import (
    get_inventory_limit_rows_by_last_id as sources_get_production_limit_rows_by_last_id,
    count_inventory as sources_count_production
)
from apps.targets.production.api import (
    count_production as targets_count_production,
    add_production as targets_add_production,
)


class ProductionsSyncResource(Resource):
    """
    ProductionsSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/productions/sync
        :return:
        """
        last_pk = '00000000-0000-0000-0000-000000000000'
        limit_num = 2000

        count_duplicate = 0

        while 1:
            inventory_rows = sources_get_production_limit_rows_by_last_id(last_pk=last_pk, limit_num=limit_num)
            if not inventory_rows:
                break
            for inventory_item in inventory_rows:

                last_pk = inventory_item.id
                source_production_id = inventory_item.id

                # 获取品牌
                production_brand = ''
                if inventory_item.productInfo:
                    enum_items_info = get_enum_items_row_by_id(inventory_item.productInfo)
                    production_brand = enum_items_info.Name.strip() if enum_items_info else ''

                production_model = inventory_item.specification.strip()

                # 判断重复
                count_dup = targets_count_production(
                    production_brand=production_brand,
                    production_model=production_model,
                )
                if count_dup:
                    count_duplicate += 1
                    print(production_brand, production_model)
                    print(count_duplicate)
                    continue
                current_time = datetime.utcnow()
                production_data = {
                    'production_brand': production_brand,
                    'production_model': inventory_item.specification,
                    'note': inventory_item.name,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                target_production_id = targets_add_production(production_data)

                # 标记关系
                contrast_data = {
                    'table_name': 'production',
                    'pk_source': source_production_id,
                    'pk_target': target_production_id,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                add_contrast(contrast_data)

        result = {
            '总数': sources_count_production(),
            '过滤重复': count_duplicate,
            '成功导入': targets_count_production(),
        }

        return jsonify(result)
