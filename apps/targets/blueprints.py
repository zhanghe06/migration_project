#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: blueprints.py
@time: 2019-04-25 18:47
"""


from flask import Blueprint

targets_bp = Blueprint('targets', __name__, url_prefix='/targets')
