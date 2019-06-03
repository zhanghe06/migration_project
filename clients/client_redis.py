#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: client_redis.py
@time: 2019-06-03 18:48
"""


import redis

from config import current_config

REDIS = current_config.REDIS

redis_client = redis.Redis(**REDIS)
