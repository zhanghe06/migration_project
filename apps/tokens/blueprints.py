#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: blueprints.py
@time: 2018-06-21 16:48
"""


from flask import Blueprint

tokens_bp = Blueprint('tokens', __name__, url_prefix='/tokens')
