#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-05-06 19:07
"""


from __future__ import unicode_literals

from datetime import datetime

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
from apps.sources.apis.current_stock import (
    get_current_stock_row_by_id as sources_get_inventory_row_by_id,
    get_current_stock_limit_rows_by_last_id as sources_get_inventory_limit_rows_by_last_id,
    count_current_stock as sources_count_inventory,
)
from apps.targets.inventory.api import (
    count_inventory as targets_count_inventory,
    add_inventory as targets_add_inventory,
    edit_inventory as targets_edit_inventory,
)
from apps.sources.apis.inventory import get_inventory_row_by_id as sources_get_production_row_by_id
from apps.targets.warehouse.api import get_warehouse_row_by_id as targets_get_warehouse_row_by_id
from apps.targets.rack.api import get_rack_row_by_id as targets_get_rack_row_by_id
from apps.targets.production.api import get_production_row_by_id as targets_get_production_row_by_id
from apps.migrations.contrast.api import (
    get_contrast_row,
    add_contrast,
)


class InventoriesSyncResource(Resource):
    """
    InventoriesSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/inventories/sync
        :return:
        """
        last_pk = '00000000-0000-0000-0000-000000000000'
        limit_num = 2000

        count_add = 0
        count_update = 0

        while 1:
            inventory_rows = sources_get_inventory_limit_rows_by_last_id(last_pk=last_pk, limit_num=limit_num)
            if not inventory_rows:
                break
            for inventory_item in inventory_rows:

                last_pk = inventory_item.id
                source_inventory_id = inventory_item.id
                target_inventory_id = 0

                # 获取目标存货
                contrast_row_inventory = get_contrast_row(table_name='inventory', pk_source=source_inventory_id)
                if contrast_row_inventory:
                    target_inventory_id = contrast_row_inventory.pk_target

                # 获取产品
                source_production_id = inventory_item.idinventory
                contrast_row_production = get_contrast_row(table_name='production', pk_source=source_production_id)
                if not contrast_row_production:
                    print('production not exist')
                    continue
                target_production_id = contrast_row_production.pk_target
                # 产品详情
                target_production = targets_get_production_row_by_id(target_production_id)
                if not target_production:
                    print('production not exist')
                    continue

                # 获取仓库
                source_warehouse_id = inventory_item.idwarehouse
                contrast_row_warehouse = get_contrast_row(table_name='warehouse', pk_source=source_warehouse_id)
                if not contrast_row_warehouse:
                    print('warehouse not exist')
                    continue
                target_warehouse_id = contrast_row_warehouse.pk_target
                # 仓库详情
                target_warehouse = targets_get_warehouse_row_by_id(target_warehouse_id)
                if not target_warehouse:
                    print('warehouse not exist')
                    continue

                # 获取仓位
                source_production = sources_get_production_row_by_id(source_production_id)
                if not source_production:
                    print('production not exist')
                    continue
                source_rack_id = source_production.idinvlocation
                contrast_row_rack = get_contrast_row(table_name='rack', pk_source=source_rack_id)
                if not contrast_row_rack:
                    print('rack not exist')
                    continue
                target_rack_id = contrast_row_rack.pk_target
                # 仓位详情
                target_rack = targets_get_rack_row_by_id(target_rack_id)
                if not target_rack:
                    print('rack not exist')
                    continue

                current_time = datetime.utcnow()
                # 新建（无历史导入记录）
                if not target_inventory_id:
                    inventory_data = {
                        'production_id': target_production_id,
                        'production_brand': target_production.production_brand,
                        'production_model': target_production.production_model,
                        'production_sku': target_production.production_sku,
                        'warehouse_id': target_warehouse_id,
                        'warehouse_name': target_warehouse.name,
                        'rack_id': target_rack_id,
                        'rack_name': target_rack.name,
                        'stock_qty_initial': inventory_item.baseQuantity,
                        'stock_qty_current': inventory_item.baseQuantity,
                        'create_time': current_time,
                        'update_time': current_time,
                    }
                    target_inventory_id = targets_add_inventory(inventory_data)

                    # 标记关系
                    contrast_data = {
                        'table_name': 'inventory',
                        'pk_source': source_inventory_id,
                        'pk_target': target_inventory_id,
                        'create_time': current_time,
                        'update_time': current_time,
                    }
                    add_contrast(contrast_data)

                    count_add += 1

                # 更新
                else:
                    inventory_data = {
                        'production_id': target_production_id,
                        'production_brand': target_production.production_brand,
                        'production_model': target_production.production_model,
                        'production_sku': target_production.production_sku,
                        'warehouse_id': target_warehouse_id,
                        'warehouse_name': target_warehouse.name,
                        'rack_id': target_rack_id,
                        'rack_name': target_rack.name,
                        'stock_qty_initial': inventory_item.baseQuantity,
                        'stock_qty_current': inventory_item.baseQuantity,
                        'update_time': current_time,
                    }
                    targets_edit_inventory(target_inventory_id, inventory_data)

                    count_update += 1

        result = {
            '来源总数': sources_count_inventory(),
            '目标总数': targets_count_inventory(),
            '新增数量': count_add,
            '更新数量': count_update,
        }

        return jsonify(result)
