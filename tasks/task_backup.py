#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: task_backup.py
@time: 2019-05-31 15:43
"""

from __future__ import print_function
from __future__ import unicode_literals

import requests
from future.moves.urllib.parse import urljoin

from apps import app
from apps.commons.requests_auth import HTTPBearerAuth
from clients.client_redis import redis_client
from tools.decorator import log_api_exception_with_desc


@log_api_exception_with_desc('数据备份')
def backup():
    url = urljoin(app.config.get('ENDPOINT'), '/backup')

    redis_prefix = app.config.get('REDIS_PREFIX')
    res_token = redis_client.get(
        '%s:%s' % (redis_prefix, 'token'),
    )
    auth = HTTPBearerAuth(res_token)

    timeout = app.config.get('TIME_OUT')

    res = requests.get(url, auth=auth, timeout=timeout)

    print(res.json())
    return True


if __name__ == '__main__':
    backup()
