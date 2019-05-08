#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: urls.py
@time: 2019-04-26 15:39
"""


from uuid import uuid4
from apps import app
from flask import jsonify, request, g, Blueprint, make_response
from apps.commons.exceptions import errors
from werkzeug import exceptions


SUCCESS_MSG = app.config['SUCCESS_MSG'].copy()


@app.before_request
def api_before_request():
    g.request_id = uuid4().get_hex()


@app.after_request
def append_request_id(response):
    response.headers.add('X-Request-Id', g.request_id)
    return response


@app.route('/', methods=['GET', 'POST', 'OPTIONS'])
def heartbeat():
    return jsonify(SUCCESS_MSG)


# 异常处理
@app.errorhandler(exceptions.NotFound.code)
def not_found(error):
    return make_response(
        jsonify(
            {
                'result': False,
                'message': error.description,
            }
        ),
        exceptions.NotFound.code
    )
