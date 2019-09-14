#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2019-09-13 09:55
"""

from __future__ import unicode_literals

from datetime import datetime

from apps.models.db_migration import Contrast as MigrationContrast
from apps.models.db_source.st_currentstock import STCurrentStock as SourceInventory
from apps.models.db_source.aa_inventory import AAInventory as SourceProduction
from apps.models.db_target import Inventory as TargetInventory
from apps.models.db_target import Production as TargetProduction
from apps.models.db_target import Rack as TargetRack
from apps.models.db_target import Warehouse as TargetWarehouse
from libs.migration_client import MigrationClient
from tools.date_time import time_local_to_utc


def sync():
    inventory_client = MigrationClient('inventory', SourceInventory, TargetInventory, MigrationContrast)
    production_client = MigrationClient('production', SourceProduction, TargetProduction, MigrationContrast)
    warehouse_client = MigrationClient('warehouse', None, TargetWarehouse, MigrationContrast)
    rack_client = MigrationClient('rack', None, TargetRack, MigrationContrast)

    while 1:
        s_rows = inventory_client.s_api.get_limit_rows_by_last_id(
            last_pk=inventory_client.s_id,
            limit_num=inventory_client.limit_num,
        )
        if not s_rows:
            break
        for s_data in s_rows:
            inventory_client.s_data = s_data
            inventory_client.s_id = inventory_client.s_data.id
            inventory_client.latest_time = time_local_to_utc(inventory_client.s_data.updated)

            # ----------
            # 产品
            production_client.m_data = production_client.m_api.get_row(
                table_name='production',
                pk_source=inventory_client.s_data.idinventory,
            )
            if not production_client.m_data:
                continue
            production_client.t_data = production_client.t_api.get_row_by_id(production_client.m_data.pk_target)
            # 仓库
            warehouse_client.m_data = warehouse_client.m_api.get_row(
                table_name='warehouse',
                pk_source=inventory_client.s_data.idwarehouse,
            )
            if not warehouse_client.m_data:
                continue
            warehouse_client.t_data = warehouse_client.t_api.get_row_by_id(warehouse_client.m_data.pk_target)
            # 仓位
            production_client.s_data = production_client.s_api.get_row_by_id(inventory_client.s_data.idinventory)
            if not production_client.s_data:
                continue
            rack_client.m_data = rack_client.m_api.get_row(
                table_name='rack',
                pk_source=production_client.s_data.idinvlocation,
            )
            if not rack_client.m_data:
                continue
            rack_client.t_data = rack_client.t_api.get_row_by_id(rack_client.m_data.pk_target)
            # ----------

            inventory_client.m_detail()
            # 存在历史数据
            if inventory_client.m_data:
                if inventory_client.latest_time <= inventory_client.m_data.latest_time:
                    continue
                # ----------
                # 更新目标数据
                inventory_client.t_id = inventory_client.m_data.pk_target
                current_time = datetime.utcnow()
                inventory_client.t_data = {
                    'production_id': production_client.t_data.id,
                    'production_brand': production_client.t_data.production_brand,
                    'production_model': production_client.t_data.production_model,
                    'production_sku': production_client.t_data.production_sku,
                    'warehouse_id': warehouse_client.t_data.id,
                    'warehouse_name': warehouse_client.t_data.name,
                    'rack_id': rack_client.t_data.id,
                    'rack_name': rack_client.t_data.name,
                    'stock_qty_initial': inventory_client.s_data.baseQuantity,
                    'stock_qty_current': inventory_client.s_data.baseQuantity,
                    'update_time': current_time,
                }
                # 删除条件
                # if inventory_client.s_data.disabled:
                #     inventory_client.t_data['status_delete'] = True
                #     inventory_client.t_data['delete_time'] = current_time
                # ----------
                inventory_client.t_update()
                inventory_client.m_update()
            # 没有历史数据
            else:
                # 目标数据去重
                inventory_client.t_data = inventory_client.t_api.get_row(
                    production_id=production_client.t_data.id,
                    warehouse_id=warehouse_client.t_data.id,
                    rack_id=rack_client.t_data.id,
                )
                if inventory_client.t_data:
                    continue
                # ----------
                # 创建目标数据
                current_time = datetime.utcnow()
                inventory_client.t_data = {
                    'production_id': production_client.t_data.id,
                    'production_brand': production_client.t_data.production_brand,
                    'production_model': production_client.t_data.production_model,
                    'production_sku': production_client.t_data.production_sku,
                    'warehouse_id': warehouse_client.t_data.id,
                    'warehouse_name': warehouse_client.t_data.name,
                    'rack_id': rack_client.t_data.id,
                    'rack_name': rack_client.t_data.name,
                    'stock_qty_initial': inventory_client.s_data.baseQuantity,
                    'stock_qty_current': inventory_client.s_data.baseQuantity,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                # 删除条件
                # if inventory_client.s_data.disabled:
                #     inventory_client.t_data['status_delete'] = True
                #     inventory_client.t_data['delete_time'] = current_time
                # ----------
                inventory_client.t_create()
                inventory_client.m_create()
    result = {
        '来源总数': inventory_client.s_api.count(),
        '目标总数': inventory_client.t_api.count(),
    }
    return result


if __name__ == '__main__':
    sync()
