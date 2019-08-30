#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2019-04-26 14:06
"""

from flask_restful import Api

from apps.migrations.blueprints import migrations_bp

migrations_api = Api(migrations_bp)
