#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_keyboard_interrupt.py
@time: 2019-09-28 21:54
"""

from tools.decorator import catch_keyboard_interrupt


@catch_keyboard_interrupt
def func():
    raise Exception('try')


class Main(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    func()
