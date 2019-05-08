#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: __init__.py.py
@time: 2019-04-25 18:44
"""


from apps.sources.blueprints import sources_bp
from flask_restful import Api
from apps.commons.exceptions import errors

sources_api = Api(sources_bp, errors=errors)
