import json
from flask import Blueprint, Response
from objects.session import Session
from objects.user import User
from security.generic import is_allowed_by_all
from security.sessions import is_valid_session
from utils import get_request_data, get_request_session, encrypt

sessions_bp = Blueprint('sessions', __name__)


@sessions_bp.route("/sessions", methods=['POST'])
@is_allowed_by_all
def create_session(**kwargs):
    """
    Authentication: is_allowed_by_all
    Authorization: None

    URL:
    None

    Body (Required):
    'email'
    'password'

    Body (Optional):
    None

    Body (Not Allowed):
    None

    Success (200): Returns created session

    Fail (40X):
    """
    email = get_request_data('email')
    password = encrypt(get_request_data('password'))

    user = User()
    user.load_by_email(email)

    if user.id and password and user.password == password:
        session = Session({'user_id': user.id})
        session.save()
        return Response(json.dumps(session.serialize()), status=200)
    else:
        return Response(json.dumps({'error': 'unable to authenticate'}), status=401)


@sessions_bp.route("/sessions/me", methods=['GET'])
@is_valid_session
def get_session(**kwargs):
    """
    Authentication: is_valid_session
    Authorization: None

    URL:
    None

    Body (Required):
    None

    Body (Optional):
    None

    Body (Not Allowed):
    None

    Success (200): Returns requested session

    Fail (40X):
    """
    return Response(json.dumps(get_request_session().serialize()), status=200)


@sessions_bp.route("/sessions/me", methods=['DELETE'])
@is_valid_session
def delete_session(**kwargs):
    """
    Authentication: is_valid_session
    Authorization: None

    URL:
    None

    Body (Required):
    None

    Body (Optional):
    None

    Body (Not Allowed):
    None

    Success (204): No content

    Fail (40X):
    """
    session = get_request_session()
    session.delete()
    return Response(json.dumps({}), status=204)
