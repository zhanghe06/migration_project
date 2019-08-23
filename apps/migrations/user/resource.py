#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: resource.py
@time: 2019-05-06 17:26
"""


from __future__ import unicode_literals

from datetime import datetime

from flask import jsonify
from flask_restful import Resource

from apps.commons.http_token_auth import token_auth
from apps.sources.apis.user import (
    get_user_row_by_id as sources_get_user_row_by_id,
    get_user_limit_rows_by_last_id as sources_get_user_limit_rows_by_last_id,
    count_user as sources_count_user,
)
from apps.targets.user.api import (
    count_user as targets_count_user,
    add_user as targets_add_user,
)
from apps.migrations.contrast.api import get_contrast_row, add_contrast


class UsersSyncResource(Resource):
    """
    UsersSyncResource
    """
    decorators = [token_auth.login_required]

    def get(self):
        """
        Example:
            curl http://0.0.0.0:5000/migrations/users/sync
        :return:
        """
        last_pk = '00000000-0000-0000-0000-000000000000'
        limit_num = 2000

        count_duplicate = 0

        while 1:
            user_rows = sources_get_user_limit_rows_by_last_id(last_pk=last_pk, limit_num=limit_num)
            if not user_rows:
                break
            for user_item in user_rows:

                last_pk = user_item.id
                source_user_id = user_item.id

                # 判断重复
                count_dup = targets_count_user(name=user_item.Code)
                if count_dup:
                    count_duplicate += 1
                    print(user_item.name)
                    print(count_duplicate)
                    continue
                current_time = datetime.utcnow()
                user_data = {
                    'name': user_item.Code,
                    'mobile': user_item.name,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                if user_item.isAdmin or user_item.issystem or user_item.isStoped:
                    user_data['status_delete'] = True,
                    user_data['delete_time'] = current_time,
                target_user_id = targets_add_user(user_data)

                # 标记关系
                contrast_data = {
                    'table_name': 'user',
                    'pk_source': source_user_id,
                    'pk_target': target_user_id,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                add_contrast(contrast_data)

        result = {
            '总数': sources_count_user(),
            '过滤重复': count_duplicate,
            '成功导入': targets_count_user(),
        }

        return jsonify(result)
