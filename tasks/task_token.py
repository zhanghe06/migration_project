#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: task_token.py
@time: 2019-06-03 18:07
"""

from __future__ import print_function
from __future__ import unicode_literals

import requests
from future.moves.urllib.parse import urljoin
from requests.auth import HTTPBasicAuth

from apps import app
from clients.client_redis import redis_client
from tools.decorator import log_api_exception_with_desc


@log_api_exception_with_desc('token 获取')
def token():
    url = urljoin(app.config.get('ENDPOINT'), '/tokens')

    username = app.config.get('BASIC_AUTH_USERNAME')
    password = app.config.get('BASIC_AUTH_PASSWORD')
    auth = HTTPBasicAuth(username, password)

    timeout = app.config.get('REQUESTS_TIME_OUT')

    res = requests.get(url, auth=auth, timeout=timeout)

    res_token = res.json().get('token')
    if not res_token:
        res_msg = res.json().get('message')
        raise Exception('token 获取失败, %s' % res_msg)
    redis_prefix = app.config.get('REDIS_PREFIX')
    res_redis = redis_client.set(
        '%s:%s' % (redis_prefix, 'token'),
        res_token,
        app.config.get('TOKEN_TTL')
    )
    return res_redis


if __name__ == '__main__':
    token()
