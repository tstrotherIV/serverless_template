import datetime
import json
import logging
import settings
from flask import request, Response, g
from functools import wraps
from objects.session import Session
from utils import get_request_session

logger = logging.getLogger()


def is_valid_session(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        logger.info("########## is_valid_session ##########")
        session_id = request.headers.get('Authorization')
        session = Session(session_id)
        if session.id:
            session_time_limit = datetime.datetime.now() - datetime.timedelta(seconds=settings.SESSION_DURATION_SECONDS)
            created_on = datetime.datetime.strptime(session.created_on, '%Y-%m-%d %H:%M:%S')
        if session.id and created_on > session_time_limit:
            logger.info("########## is_valid_session: success")
            g.authenticated = True
            g.session = session
            return f(*args, **kwargs)
        else:
            logger.info("########## is_valid_session: failure")
            return Response(json.dumps({'message': 'unable to authenticate'}), status=401)
    return wrapped


def target_user_is_session_user(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        logger.info("########## is_session_user ##########")
        if get_request_session().user_id == kwargs['user_id']:
            logger.info("########## is_session_user: success")
            return f(*args, **kwargs)
        else:
            logger.info("########## is_session_user: failure")
            return Response(json.dumps({'message': 'unable to authorize'}), status=403)
    return wrapped
