#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2019-09-13 09:02
"""

from __future__ import unicode_literals

from datetime import datetime

from apps.models.db_migration import Contrast as MigrationContrast
from apps.models.db_source.aa_inventory import AAInventory as SourceProduction
from apps.models.db_source.eap_enumitem import EapEnumItem as SourceBrand
from apps.models.db_target import Production as TargetProduction
from libs.migration_client import MigrationClient
from tools.date_time import time_local_to_utc


def sync():
    production_client = MigrationClient('production', SourceProduction, TargetProduction, MigrationContrast)
    brand_client = MigrationClient('brand', s_model=SourceBrand)

    while 1:
        s_rows = production_client.s_api.get_limit_rows_by_last_id(
            last_pk=production_client.s_id,
            limit_num=production_client.limit_num,
        )
        if not s_rows:
            break
        for s_data in s_rows:
            production_client.s_data = s_data
            production_client.s_id = production_client.s_data.id
            production_client.latest_time = time_local_to_utc(production_client.s_data.updated)

            # ----------
            production_brand = ''
            if s_data.productInfo:
                s_data_brand = brand_client.s_api.get_row_by_id(s_data.productInfo)
                production_brand = s_data_brand.Name.strip().upper() if s_data_brand else ''
            production_model = s_data.specification.strip().upper()
            # ----------

            production_client.m_detail()
            # 存在历史数据
            if production_client.m_data:
                if production_client.latest_time <= production_client.m_data.latest_time:
                    continue
                # ----------
                # 更新目标数据
                production_client.t_id = production_client.m_data.pk_target
                current_time = datetime.utcnow()
                production_client.t_data = {
                    'production_brand': production_brand,
                    'production_model': production_model,
                    'note': production_client.s_data.name,
                    'cost_ref': production_client.s_data.invSCost,
                    'cost_new': production_client.s_data.latestCost,
                    'cost_avg': production_client.s_data.avagCost,
                    'update_time': current_time,
                }
                # 删除条件
                if production_client.s_data.disabled:
                    production_client.t_data['status_delete'] = True
                    production_client.t_data['delete_time'] = current_time
                # ----------
                production_client.t_update()
                production_client.m_update()
            # 没有历史数据
            else:
                # 目标数据去重
                production_client.t_data = production_client.t_api.get_row(
                    production_brand=production_brand,
                    production_model=production_model,
                )
                if production_client.t_data:
                    continue
                # ----------
                # 创建目标数据
                current_time = datetime.utcnow()
                production_client.t_data = {
                    'production_brand': production_brand,
                    'production_model': production_model,
                    'note': production_client.s_data.name,
                    'cost_ref': production_client.s_data.invSCost,
                    'cost_new': production_client.s_data.latestCost,
                    'cost_avg': production_client.s_data.avagCost,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                # 删除条件
                if production_client.s_data.disabled:
                    production_client.t_data['status_delete'] = True
                    production_client.t_data['delete_time'] = current_time
                # ----------
                production_client.t_create()
                production_client.m_create()
    result = {
        '来源总数': production_client.s_api.count(),
        '目标总数': production_client.t_api.count(),
    }
    return result


if __name__ == '__main__':
    sync()
