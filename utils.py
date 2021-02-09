import hashlib
import json
import logging
from flask import request, g

logger = logging.getLogger()


def get_request_session():
    return g.session


def get_request_method():
    return request.method


def get_request_headers(key=None, default=''):
    if key:
        if request.headers:
            return request.headers.get(key, default)
        else:
            return default
    else:
        if request.headers:
            return request.headers
        else:
            if default != '':
                return default
            else:
                return {}


def get_request_data(key=None, default=''):
    if key:
        if request.data:
            return json.loads(request.data).get(key, default)
        else:
            return default
    else:
        if request.data:
            return json.loads(request.data)
        else:
            if default != '':
                return default
            else:
                return {}


def get_request_args(key=None):
    if key:
        return request.args.get(key)
    else:
        return request.args


def get_request_url():
    return request.url


def encrypt(string):
    return hashlib.sha256(string.encode()).hexdigest()
