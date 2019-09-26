#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2019-09-06 21:02
"""

from __future__ import unicode_literals

from datetime import datetime

from apps.models.db_migration import Contrast as MigrationContrast
from apps.models.db_source.aa_inventorylocation import AAInventoryLocation as SourceRack
from apps.models.db_target import Rack as TargetRack
from libs.migration_client import MigrationClient
from tools.date_time import time_local_to_utc


def sync():
    rack_client = MigrationClient('rack', SourceRack, TargetRack, MigrationContrast)

    while 1:
        s_rows = rack_client.s_api.get_limit_rows_by_last_id(
            last_pk=rack_client.s_id,
            limit_num=rack_client.limit_num,
        )
        if not s_rows:
            break
        for s_data in s_rows:
            rack_client.s_data = s_data
            rack_client.s_id = rack_client.s_data.id
            rack_client.latest_time = time_local_to_utc(rack_client.s_data.updated)

            # ----------
            m_data_warehouse = rack_client.m_api.get_row(
                table_name='warehouse',
                pk_source=rack_client.s_data.idwarehouse,
            )
            if not m_data_warehouse:
                continue
            # ----------

            rack_client.m_detail()
            # 存在历史数据
            if rack_client.m_data:
                if not rack_client.s_data.updated:
                    continue
                if rack_client.latest_time <= rack_client.m_data.latest_time:
                    continue
                # ----------
                # 更新目标数据
                rack_client.t_id = rack_client.m_data.pk_target
                current_time = datetime.utcnow()
                rack_client.t_data = {
                    'name': rack_client.s_data.name,
                    'warehouse_id': m_data_warehouse.pk_target,
                    'update_time': current_time,
                }
                # 删除条件
                if rack_client.s_data.disabled:
                    rack_client.t_data['status_delete'] = True
                    rack_client.t_data['delete_time'] = current_time
                # ----------
                rack_client.t_update()
                rack_client.m_update()
            # 没有历史数据
            else:
                # 目标数据去重
                rack_client.t_data = rack_client.t_api.get_row(name=rack_client.s_data.name)
                if rack_client.t_data:
                    continue
                # ----------
                # 创建目标数据
                current_time = datetime.utcnow()
                rack_client.t_data = {
                    'name': rack_client.s_data.name,
                    'warehouse_id': m_data_warehouse.pk_target,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                # 删除条件
                if rack_client.s_data.disabled:
                    rack_client.t_data['status_delete'] = True
                    rack_client.t_data['delete_time'] = current_time
                # ----------
                rack_client.t_create()
                rack_client.m_create()
    result = {
        '来源总数': rack_client.s_api.count(),
        '目标总数': rack_client.t_api.count(),
    }
    return result


if __name__ == '__main__':
    sync()
