#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: blueprints.py
@time: 2019-04-25 18:47
"""

from flask import Blueprint

migrations_bp = Blueprint('migrations', __name__, url_prefix='/migrations')
