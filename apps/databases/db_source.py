#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: db_source.py
@time: 2019-04-26 01:25
"""

from flask_sqlalchemy import SQLAlchemy

from apps import app


def get_source_db():
    return SQLAlchemy(app)


source_db = get_source_db()
