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
from apps.migrations.contrast.api import add_contrast, get_contrast_row
from apps.sources.apis.enum_items import get_enum_items_row_by_id
from apps.sources.apis.inventory import (
    get_inventory_limit_rows_by_last_id as sources_get_production_limit_rows_by_last_id,
    count_inventory as sources_count_production
)
from apps.targets.production.api import (
    count_production as targets_count_production,
    add_production as targets_add_production,
    edit_production as targets_edit_production,
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

        count_add = 0
        count_update = 0
        count_duplicate = 0

        while 1:
            production_rows = sources_get_production_limit_rows_by_last_id(last_pk=last_pk, limit_num=limit_num)
            if not production_rows:
                break
            for production_item in production_rows:

                last_pk = production_item.id
                source_production_id = production_item.id
                target_production_id = 0

                # 获取目标产品
                contrast_row_production = get_contrast_row(table_name='production', pk_source=source_production_id)
                if contrast_row_production:
                    target_production_id = contrast_row_production.pk_target

                # 获取品牌
                production_brand = ''
                if production_item.productInfo:
                    enum_items_info = get_enum_items_row_by_id(production_item.productInfo)
                    production_brand = enum_items_info.Name.strip() if enum_items_info else ''

                production_model = production_item.specification.strip()

                current_time = datetime.utcnow()
                # 新建（无历史导入记录）
                if not target_production_id:
                    # 判断重复
                    count_dup = targets_count_production(
                        production_brand=production_brand,
                        production_model=production_model,
                    )
                    if count_dup:
                        count_duplicate += 1
                        print('duplicate:', production_brand, production_model)
                        continue

                    production_data = {
                        'production_brand': production_brand,
                        'production_model': production_item.specification,
                        'note': production_item.name,
                        'cost_ref': production_item.invSCost,
                        'cost_new': production_item.latestCost,
                        'cost_avg': production_item.avagCost,
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

                    count_add += 1

                # 更新
                else:
                    production_data = {
                        'production_brand': production_brand,
                        'production_model': production_item.specification,
                        'note': production_item.name,
                        'cost_ref': production_item.invSCost,
                        'cost_new': production_item.latestCost,
                        'cost_avg': production_item.avagCost,
                        'create_time': current_time,
                        'update_time': current_time,
                    }
                    targets_edit_production(target_production_id, production_data)

                    count_update += 1

        result = {
            '来源总数': sources_count_production(),
            '目标总数': targets_count_production(),
            '新增数量': count_add,
            '更新数量': count_update,
            '过滤重复': count_duplicate,
        }

        return jsonify(result)
