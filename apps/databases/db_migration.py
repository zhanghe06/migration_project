#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: db_migration.py
@time: 2019-04-26 01:42
"""

from flask_sqlalchemy import SQLAlchemy

from apps import app


def get_migration_db():
    return SQLAlchemy(app)


migration_db = get_migration_db()
