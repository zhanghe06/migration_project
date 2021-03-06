#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: db_target.py
@time: 2019-04-26 01:26
"""

from flask_sqlalchemy import SQLAlchemy

from apps import app


def get_target_db():
    return SQLAlchemy(app)


target_db = SQLAlchemy(app)

# SQLALCHEMY_ENGINE_OPTIONS
