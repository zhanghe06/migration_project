#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_datetime.py
@time: 2019-08-22 20:07
"""

from tools.date_time import time_local_to_utc


def test():
    utc_time = time_local_to_utc('2017-06-16 11:21:01')
    print(utc_time)
    print(type(utc_time))


if __name__ == '__main__':
    test()
