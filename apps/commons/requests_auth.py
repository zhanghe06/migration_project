#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: requests_auth.py
@time: 2019-06-03 23:39
"""


from requests.auth import AuthBase


class HTTPBearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __eq__(self, other):
        return self.token == getattr(other, 'token', None)

    def __ne__(self, other):
        return not self == other

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.token
        return r


if __name__ == '__main__':
    pass
