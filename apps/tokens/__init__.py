#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2018-06-21 16:45
"""


from apps.tokens.blueprints import tokens_bp
from flask_restful import Api
from apps.commons.exceptions import errors

tokens_api = Api(tokens_bp, errors=errors)
