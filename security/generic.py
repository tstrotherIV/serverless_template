import logging
from flask import g
from functools import wraps

logger = logging.getLogger()


def is_allowed_by_all(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        g.authenticated = True
        return f(*args, **kwargs)
    return wrapped
