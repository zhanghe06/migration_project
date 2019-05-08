#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2018-06-21 16:48
"""


from apps.tokens.resources import TokenResource

from apps.tokens import tokens_api


tokens_api.add_resource(TokenResource, '/', endpoint='tokens', strict_slashes=False)
