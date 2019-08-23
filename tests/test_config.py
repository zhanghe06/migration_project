#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_config.py
@time: 2019-06-03 19:48
"""
from apps import app


def test_conf_quote():
    """引用"""
    print(app.config['SUCCESS_MSG'])
    success_msg = app.config['SUCCESS_MSG']
    success_msg['message'] = '123'
    print(app.config['SUCCESS_MSG'])


def test_conf_copy():
    """拷贝"""
    print(app.config['SUCCESS_MSG'])
    success_msg = app.config['SUCCESS_MSG'].copy()
    success_msg['message'] = '456'
    print(app.config['SUCCESS_MSG'])


if __name__ == '__main__':
    test_conf_quote()
    test_conf_copy()
