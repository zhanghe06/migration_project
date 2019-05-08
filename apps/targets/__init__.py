#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2019-04-25 18:45
"""


from apps.targets.blueprints import targets_bp
from flask_restful import Api

targets_api = Api(targets_bp)
