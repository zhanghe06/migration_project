#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: migration_client.py
@time: 2019-09-11 17:35
"""

from __future__ import unicode_literals

from datetime import datetime

from apps import app
from apps.databases.db_migration import get_migration_db
from apps.databases.db_source import get_source_db
from apps.databases.db_target import get_target_db
from libs.db_orm_api import DbApi


class MigrationClient(object):
    s_id = app.config['SYNC_LAST_PK']
    t_id = None
    m_id = None

    s_data = None
    t_data = None
    m_data = None

    latest_time = None
    limit_num = app.config['SYNC_LIMIT_NUM']

    def __init__(self, table_name, s_model=None, t_model=None, m_model=None):
        self.table_name = table_name
        self.s_api = DbApi(get_source_db(), s_model)
        self.t_api = DbApi(get_target_db(), t_model)
        self.m_api = DbApi(get_migration_db(), m_model)

    def t_create(self):
        self.t_id = self.t_api.add(self.t_data)

    def t_update(self):
        self.t_api.edit(self.t_id, self.t_data)

    def m_detail(self):
        self.m_data = self.m_api.get_row(
            table_name=self.table_name,
            pk_source=self.s_id,
        )

    def m_create(self):
        current_time = datetime.utcnow()
        m_data = {
            'table_name': self.table_name,
            'pk_source': self.s_id,
            'pk_target': self.t_id,
            'latest_time': self.latest_time,
            'create_time': current_time,
            'update_time': current_time,
        }
        self.m_id = self.m_api.add(m_data)

    def m_update(self):
        current_time = datetime.utcnow()
        m_data = {
            'table_name': self.table_name,
            'pk_source': self.s_id,
            'pk_target': self.t_id,
            'latest_time': self.latest_time,
            'create_time': current_time,
            'update_time': current_time,
        }
        self.m_api.edit(self.m_id, m_data)
