#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2019-08-30 11:02
"""

from __future__ import unicode_literals

from datetime import datetime

from apps.models.db_migration import Contrast as MigrationContrast
from apps.models.db_source.aa_warehouse import AAWarehouse as SourceWarehouse
from apps.models.db_target import Warehouse as TargetWarehouse
from libs.migration_client import MigrationClient
from tools.date_time import time_local_to_utc


def sync():
    warehouse_client = MigrationClient('warehouse', SourceWarehouse, TargetWarehouse, MigrationContrast)

    while 1:
        s_rows = warehouse_client.s_api.get_limit_rows_by_last_id(
            last_pk=warehouse_client.s_id,
            limit_num=warehouse_client.limit_num,
        )
        if not s_rows:
            break
        for s_data in s_rows:
            warehouse_client.s_data = s_data
            warehouse_client.s_id = warehouse_client.s_data.id
            warehouse_client.latest_time = time_local_to_utc(warehouse_client.s_data.updated)

            warehouse_client.m_detail()
            # 存在历史数据
            if warehouse_client.m_data:
                if not warehouse_client.s_data.updated:
                    continue
                if warehouse_client.latest_time <= warehouse_client.m_data.latest_time:
                    continue
                # ----------
                # 更新目标数据
                warehouse_client.t_id = warehouse_client.m_data.pk_target
                current_time = datetime.utcnow()
                warehouse_client.t_data = {
                    'name': warehouse_client.s_data.name,
                    'address': warehouse_client.s_data.address,
                    'update_time': current_time,
                }
                # 删除条件
                if warehouse_client.s_data.disabled:
                    warehouse_client.t_data['status_delete'] = True
                    warehouse_client.t_data['delete_time'] = current_time
                # ----------
                warehouse_client.t_update()
                warehouse_client.m_update()
            # 没有历史数据
            else:
                # 目标数据去重
                warehouse_client.t_data = warehouse_client.t_api.get_row(name=warehouse_client.s_data.name)
                if warehouse_client.t_data:
                    continue
                # ----------
                # 创建目标数据
                current_time = datetime.utcnow()
                warehouse_client.t_data = {
                    'name': warehouse_client.s_data.name,
                    'address': warehouse_client.s_data.address,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                # 删除条件
                if warehouse_client.s_data.disabled:
                    warehouse_client.t_data['status_delete'] = True
                    warehouse_client.t_data['delete_time'] = current_time
                # ----------
                warehouse_client.t_create()
                warehouse_client.m_create()
    result = {
        '来源总数': warehouse_client.s_api.count(),
        '目标总数': warehouse_client.t_api.count(),
    }
    return result


if __name__ == '__main__':
    sync()
