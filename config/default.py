#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: default.py
@time: 2019-04-25 18:16
"""

from __future__ import print_function
from __future__ import unicode_literals

import os
import binascii

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

HOST = '0.0.0.0'
PORT = 8000
DEBUG = True
SECRET_KEY = 'c9a6b2eb758aab3e1899576e76d72550cb3dd6d7a4b56b66'

TOKEN_TTL = 600

# requests 超时设置
REQUESTS_TIME_OUT = (30, 30)
MIGRATION_TIME_OUT = (30*60, 30*60)

# 数据库 MsSQL - 来源
DB_MSSQL_SOURCE = {
    'host': '%s\SQLEXPRESS' % HOST,
    'username': 'sa',
    'password': '1qazXSW@',
    'port': 1433,
    'db': 'db_source'
}
SQLALCHEMY_DATABASE_URI_SOURCE = \
    'mssql+pymssql://%(username)s:%(password)s@%(host)s/%(db)s?charset=utf8' % DB_MSSQL_SOURCE

# 数据库 MySQL - 目标
DB_MYSQL_TARGET = {
    'host': HOST,
    'user': 'root',
    'passwd': '123456',
    'port': 3306,
    'db': 'db_target'
}

SQLALCHEMY_DATABASE_URI_TARGET = \
    'mysql+mysqldb://%(user)s:%(passwd)s@%(host)s:%(port)s/%(db)s?charset=utf8mb4' % DB_MYSQL_TARGET

# 数据库 MySQL - 迁移
DB_MYSQL = {
    'host': HOST,
    'user': 'root',
    'passwd': '123456',
    'port': 3306,
    'db': 'migration_project'
}

SQLALCHEMY_DATABASE_URI = \
    'mysql+mysqldb://%(user)s:%(passwd)s@%(host)s:%(port)s/%(db)s?charset=utf8mb4' % DB_MYSQL

SQLALCHEMY_BINDS = {
    'db_source': SQLALCHEMY_DATABASE_URI_SOURCE,
    'db_target': SQLALCHEMY_DATABASE_URI_TARGET,
    'db_migration': SQLALCHEMY_DATABASE_URI
}

SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_POOL_SIZE = 5  # 默认 pool_size=5
# SQLALCHEMY_MAX_OVERFLOW = 10  # 默认 10 连接池达到最大值后可以创建的连接数
# SQLALCHEMY_POOL_TIMEOUT = 10  # 默认 10秒
SQLALCHEMY_POOL_RECYCLE = 500  # 配置要小于 数据库配置 wait_timeout
SQLALCHEMY_ECHO = False

# 缓存，队列
REDIS = {
    'host': HOST,
    'port': 6379,
    # 'password': '123456'  # redis-cli AUTH 123456
}

REDIS_URL = 'redis://:%s@%s' % (REDIS['password'], REDIS['host']) \
    if REDIS.get('password') else 'redis://%s' % REDIS['host']

REDIS_PREFIX = 'migration'

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

SUCCESS_MSG = {
    'result': True,
    'message': '',
}

FAILURE_MSG = {
    'result': False,
    'message': '',
}

# Basic Auth
BASIC_AUTH_USERNAME = 'username'
BASIC_AUTH_PASSWORD = 'password'

# Endpoint
ENDPOINT = 'http://%s:%s' % (HOST, PORT)


if __name__ == '__main__':
    sk = os.urandom(24)
    print(sk)
    print(binascii.b2a_hex(sk))
