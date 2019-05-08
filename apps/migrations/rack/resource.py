#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-05-05 17:29
"""


from __future__ import unicode_literals

from datetime import datetime

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
from apps.sources.apis.rack import (
    get_rack_row_by_id as sources_get_rack_row_by_id,
    get_rack_limit_rows_by_last_id as sources_get_rack_limit_rows_by_last_id,
    count_rack as sources_count_rack,
)
from apps.targets.rack.api import (
    count_rack as targets_count_rack,
    add_rack as targets_add_rack,
)
from apps.migrations.contrast.api import get_contrast_row, add_contrast


class RacksSyncResource(Resource):
    """
    RacksSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/racks/sync
        :return:
        """
        last_pk = '00000000-0000-0000-0000-000000000000'
        limit_num = 2000

        count_duplicate = 0

        while 1:
            rack_rows = sources_get_rack_limit_rows_by_last_id(last_pk=last_pk, limit_num=limit_num)
            if not rack_rows:
                break
            for rack_item in rack_rows:

                last_pk = rack_item.id
                source_rack_id = rack_item.id

                # 判断重复
                count_dup = targets_count_rack(name=rack_item.name)
                if count_dup:
                    count_duplicate += 1
                    print(rack_item.name)
                    print(count_duplicate)
                    continue
                source_warehouse_id = rack_item.idwarehouse
                contrast_row_warehouse = get_contrast_row(table_name='warehouse', pk_source=source_warehouse_id)
                if not contrast_row_warehouse:
                    print('warehouse not exist')
                    continue
                target_warehouse_id = contrast_row_warehouse.pk_target
                current_time = datetime.utcnow()
                rack_data = {
                    'name': rack_item.name,
                    'warehouse_id': target_warehouse_id,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                if rack_item.disabled:
                    rack_data['status_delete'] = True,
                    rack_data['delete_time'] = current_time,
                target_rack_id = targets_add_rack(rack_data)

                # 标记关系
                contrast_data = {
                    'table_name': 'rack',
                    'pk_source': source_rack_id,
                    'pk_target': target_rack_id,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                add_contrast(contrast_data)

        result = {
            '总数': sources_count_rack(),
            '过滤重复': count_duplicate,
            '成功导入': targets_count_rack(),
        }

        return jsonify(result)
