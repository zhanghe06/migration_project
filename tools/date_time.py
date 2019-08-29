#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: date_time.py
@time: 2019-08-23 13:49
"""

from __future__ import unicode_literals

import time
from datetime import datetime, timedelta, date

import six


def time_local_to_utc(local_time):
    """
    本地时间转UTC时间
    :param local_time:
    :return:
    """
    # 字符串处理
    if isinstance(local_time, six.string_types) and len(local_time) == 10:
        local_time = datetime.strptime(local_time, '%Y-%m-%d')
    elif isinstance(local_time, six.string_types) and len(local_time) >= 19:
        local_time = datetime.strptime(local_time[:19], '%Y-%m-%d %H:%M:%S')
    elif not (isinstance(local_time, datetime) or isinstance(local_time, date)):
        local_time = datetime.now()
    # 时间转换
    utc_time = local_time + timedelta(seconds=time.timezone)
    return utc_time


def time_utc_to_local(utc_time):
    """
    UTC时间转本地时间
    :param utc_time:
    :return:
    """
    # 字符串处理
    if isinstance(utc_time, six.string_types) and len(utc_time) == 10:
        utc_time = datetime.strptime(utc_time, '%Y-%m-%d')
    elif isinstance(utc_time, six.string_types) and len(utc_time) >= 19:
        utc_time = datetime.strptime(utc_time[:19], '%Y-%m-%d %H:%M:%S')
    elif not (isinstance(utc_time, datetime) or isinstance(utc_time, date)):
        utc_time = datetime.utcnow()
    # 时间转换
    local_time = utc_time - timedelta(seconds=time.timezone)
    return local_time
