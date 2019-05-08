#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: exceptions.py
@time: 2019-04-26 20:07
"""

from werkzeug.exceptions import (
    Unauthorized,
    Forbidden,
    Conflict,
    Gone,
    Locked,
    BadRequest,
    NotFound,
    MethodNotAllowed,
    PreconditionFailed,
    RequestEntityTooLarge,
    UnsupportedMediaType,
    ServiceUnavailable,
)


# 自定义 TOKEN 异常
class TokenNotExist(Forbidden):
    description = 'Token required.'


class TokenExpired(Forbidden):
    description = 'Token expired.'


class TokenError(Forbidden):
    description = 'Token error.'


errors = {
    BadRequest.name: {
        'message': BadRequest.description or 'Bad request.',
        'status': BadRequest.code,
    },
    Unauthorized.name: {
        'message': Unauthorized.description or 'Authentication required.',
        'status': Unauthorized.code,
    },
    Forbidden.name: {
        'message': Forbidden.description or 'Forbidden.',
        'status': Forbidden.code,
    },
    TokenNotExist.name: {
        'message': TokenNotExist.description or 'Token required.',
        'status': TokenNotExist.code or Forbidden.code,
    },
    TokenExpired.name: {
        'message': TokenExpired.description or 'Token expired.',
        'status': TokenExpired.code or Forbidden.code,
    },
    TokenError.name: {
        'message': TokenError.description or 'Token error.',
        'status': TokenError.code or Forbidden.code,
    },
    NotFound.name: {
        'message': NotFound.description or 'Not found.',
        'status': NotFound.code,
    },
    MethodNotAllowed.name: {
        'message': MethodNotAllowed.description or 'Method not allowed.',
        'status': MethodNotAllowed.code,
    },
    Conflict.name: {
        'message': Conflict.description or 'Conflict, Resource already exists.',
        'status': Conflict.code,
    },
    Gone.name: {
        'message': Gone.description or 'Gone, Resource is gone.',
        'status': Gone.code,
    },
    Locked.name: {
        'message': Locked.description or 'Locked, Resource is locked.',
        'status': Locked.code,
    },
    PreconditionFailed.name: {
        'message': PreconditionFailed.description or 'Precondition failed.',
        'status': PreconditionFailed.code,
    },
    RequestEntityTooLarge.name: {
        'message': RequestEntityTooLarge.description or 'Request entity too large.',
        'status': RequestEntityTooLarge.code,
    },
    UnsupportedMediaType.name: {
        'message': UnsupportedMediaType.description or 'Unsupported media type.',
        'status': UnsupportedMediaType.code,
    },
    ServiceUnavailable.name: {
        'message': ServiceUnavailable.description or 'Service unavailable.',
        'status': ServiceUnavailable.code,
    },
}
