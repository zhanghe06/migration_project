#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: test_decorator.py
@time: 2019-09-03 17:48
"""


from __future__ import print_function
from __future__ import unicode_literals

from tools.decorator import log_api_exception_with_desc


@log_api_exception_with_desc('中文测试')
def test():
    print(' '.join(['中文测试', '中文测试']))


if __name__ == '__main__':
    test()
