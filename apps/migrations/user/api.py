#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: api.py
@time: 2019-09-14 14:34
"""


from __future__ import unicode_literals

from datetime import datetime

from apps.models.db_migration import Contrast as MigrationContrast
from apps.models.db_source.eap_user import EAPUser as SourceUser
from apps.models.db_target import User as TargetUser
from libs.migration_client import MigrationClient
from tools.date_time import time_local_to_utc


def sync():
    user_client = MigrationClient('user', SourceUser, TargetUser, MigrationContrast)

    while 1:
        s_rows = user_client.s_api.get_limit_rows_by_last_id(
            last_pk=user_client.s_id,
            limit_num=user_client.limit_num,
        )
        if not s_rows:
            break
        for s_data in s_rows:
            user_client.s_data = s_data
            user_client.s_id = user_client.s_data.id
            user_client.latest_time = time_local_to_utc(user_client.s_data.updated)

            user_client.m_detail()
            # 存在历史数据
            if user_client.m_data:
                if user_client.latest_time <= user_client.m_data.latest_time:
                    continue
                # ----------
                # 更新目标数据
                user_client.t_id = user_client.m_data.pk_target
                current_time = datetime.utcnow()
                user_client.t_data = {
                    'name': user_client.s_data.Code,
                    'mobile': user_client.s_data.name,
                    'update_time': current_time,
                }
                # 删除条件
                if user_client.s_data.issystem or user_client.s_data.isStoped:
                    user_client.t_data['status_delete'] = True
                    user_client.t_data['delete_time'] = current_time
                # ----------
                user_client.t_update()
                user_client.m_update()
            # 没有历史数据
            else:
                # 目标数据去重
                user_client.t_data = user_client.t_api.get_row(name=user_client.s_data.Code)
                if user_client.t_data:
                    continue
                # ----------
                # 创建目标数据
                current_time = datetime.utcnow()
                user_client.t_data = {
                    'name': user_client.s_data.Code,
                    'mobile': user_client.s_data.name,
                    'create_time': current_time,
                    'update_time': current_time,
                }
                # 删除条件
                if user_client.s_data.issystem or user_client.s_data.isStoped:
                    user_client.t_data['status_delete'] = True
                    user_client.t_data['delete_time'] = current_time
                # ----------
                user_client.t_create()
                user_client.m_create()
    result = {
        '来源总数': user_client.s_api.count(),
        '目标总数': user_client.t_api.count(),
    }
    return result


if __name__ == '__main__':
    sync()
