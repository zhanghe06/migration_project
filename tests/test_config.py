#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_config.py
@time: 2019-06-03 19:48
"""
from apps import app


def func():
    print(app.config['SUCCESS_MSG'])
    SUCCESS_MSG = app.config['SUCCESS_MSG'].copy()
    SUCCESS_MSG['message'] = '123'
    print(app.config['SUCCESS_MSG'])


class Main(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    func()
