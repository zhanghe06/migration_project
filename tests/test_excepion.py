#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_excepion.py
@time: 2019-06-03 22:42
"""


def func():
    try:
        print('try')
        raise Exception('try')
    except Exception as e:
        print('except')
        raise Exception(e)
    finally:
        print('finally')


class Main(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    func()
