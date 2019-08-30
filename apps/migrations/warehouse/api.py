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

from apps.migrations.contrast.api import add_contrast
from apps.sources.apis.warehouse import (
    get_warehouse_limit_rows_by_last_id as sources_get_warehouse_limit_rows_by_last_id,
    count_warehouse as sources_count_warehouse,
)
from apps.targets.warehouse.api import (
    count_warehouse as targets_count_warehouse,
    add_warehouse as targets_add_warehouse,
)


def sync():
    last_pk = '00000000-0000-0000-0000-000000000000'
    limit_num = 2000

    count_duplicate = 0

    while 1:
        warehouse_rows = sources_get_warehouse_limit_rows_by_last_id(last_pk=last_pk, limit_num=limit_num)
        if not warehouse_rows:
            break
        for warehouse_item in warehouse_rows:

            last_pk = warehouse_item.id
            source_warehouse_id = warehouse_item.id

            # 判断重复
            count_dup = targets_count_warehouse(name=warehouse_item.name)
            if count_dup:
                count_duplicate += 1
                print(warehouse_item.name)
                print(count_duplicate)
                continue
            current_time = datetime.utcnow()
            warehouse_data = {
                'name': warehouse_item.name,
                'address': warehouse_item.address,
                'create_time': current_time,
                'update_time': current_time,
            }
            if warehouse_item.disabled:
                warehouse_data['status_delete'] = True,
                warehouse_data['delete_time'] = current_time,
            target_warehouse_id = targets_add_warehouse(warehouse_data)

            # 标记关系
            contrast_data = {
                'table_name': 'warehouse',
                'pk_source': source_warehouse_id,
                'pk_target': target_warehouse_id,
                'create_time': current_time,
                'update_time': current_time,
            }
            add_contrast(contrast_data)

    result = {
        '总数': sources_count_warehouse(),
        '过滤重复': count_duplicate,
        '成功导入': targets_count_warehouse(),
    }
    return result


if __name__ == '__main__':
    sync()
