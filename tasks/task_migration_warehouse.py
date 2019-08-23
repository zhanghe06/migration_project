#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: task_migration_warehouse.py
@time: 2019-05-31 15:43
"""


from __future__ import print_function
from __future__ import unicode_literals

import requests
from future.moves.urllib.parse import urljoin
from apps.commons.requests_auth import HTTPBearerAuth

from apps import app
from clients.client_redis import redis_client
from tools.decorator import log_api_exception_with_desc


@log_api_exception_with_desc('仓库信息同步')
def migration_warehouse():
    url = urljoin(app.config.get('ENDPOINT'), '/migrations/warehouses/sync')

    redis_prefix = app.config.get('REDIS_PREFIX')
    res_token = redis_client.get(
        '%s:%s' % (redis_prefix, 'token'),
    )
    auth = HTTPBearerAuth(res_token)

    timeout = app.config.get('MIGRATION_TIME_OUT')

    res = requests.get(url, auth=auth, timeout=timeout)

    print(res.json())
    return True


if __name__ == '__main__':
    migration_warehouse()
