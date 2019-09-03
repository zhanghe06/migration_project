#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: decorator.py
@time: 2019-05-31 15:49
"""

from __future__ import print_function
from __future__ import unicode_literals

import time
from functools import wraps


def catch_keyboard_interrupt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print('\n强制退出')

    return wrapper


def log_api_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            func_res = func(*args, **kwargs)
            return func_res
        except Exception as e:
            print(e.message)
        finally:
            end_time = time.time()
            run_time = end_time - start_time
            msg = '%s.%s 运行时间: %0.2fS' % (func.__module__, func.__name__, run_time)
            print(msg)

    return wrapper


def log_api_exception_with_desc(desc=''):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                func_res = func(*args, **kwargs)
                return func_res
            except Exception as e:
                print(e.message)
            finally:
                end_time = time.time()
                run_time = end_time - start_time
                msg = '%s.%s 运行时间: %0.2fS' % (func.__module__, func.__name__, run_time)
                print(' '.join([time.strftime('%Y-%m-%d %H:%M:%S'), desc, msg]))

        return wrapper

    return decorator


def sleep_decorator(second):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('{} sleep {} s'.format(func.__name__, second))
            time.sleep(second)
            func_res = func(*args, **kwargs)
            return func_res

        return wrapper

    return decorator
