#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: date_time.py
@time: 2019-08-23 13:49
"""

import time

from datetime import datetime, timedelta, date


def time_local_to_utc(local_time):
    """
    本地时间转UTC时间
    :param local_time:
    :return:
    """
    # 字符串处理
    if isinstance(local_time, str) and len(local_time) == 10:
        local_time = datetime.strptime(local_time, '%Y-%m-%d')
    elif isinstance(local_time, str) and len(local_time) >= 19:
        local_time = datetime.strptime(local_time[:19], '%Y-%m-%d %H:%M:%S')
    elif not (isinstance(local_time, datetime) or isinstance(local_time, date)):
        local_time = datetime.now()
    # 时间转换
    utc_time = local_time + timedelta(seconds=time.timezone)
    return utc_time
