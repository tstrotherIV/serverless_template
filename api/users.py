import json
from flask import Blueprint, Response
from objects.abstract_model_object import RequiredAttributes
from objects.user import User, EmailExists
from security.generic import is_allowed_by_all
from security.sessions import is_valid_session, target_user_is_session_user
from utils import get_request_data, encrypt

users_bp = Blueprint('users', __name__)


@users_bp.route("/users", methods=['POST'])
@is_allowed_by_all
def create_user(**kwargs):
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

    Success (200): Returns created user

    Fail (40X):
    """
    try:
        user = User(get_request_data())
        if user.password:
            user.password = encrypt(user.password)
        user.save()
    except (AttributeError, RequiredAttributes, EmailExists) as e:
        return Response(json.dumps({'error': str(e)}), status=400)

    return Response(json.dumps(user.serialize()), status=200)


@users_bp.route("/users/<user_id>", methods=['GET'])
@is_valid_session
@target_user_is_session_user
def get_user(user_id, **kwargs):
    """
    Authentication: is_valid_session
    Authorization: target_user_is_session_user

    URL:
    <user_id>: Target user id

    Success (200): Returns requested user

    Fail (40X):
    """
    user = User(user_id)
    return Response(json.dumps(user.serialize()), status=200)


@users_bp.route("/users/<user_id>", methods=['PATCH'])
@is_valid_session
@target_user_is_session_user
def update_user(user_id, **kwargs):
    """
    Authentication: is_valid_session
    Authorization: target_user_is_session_user

    URL:
    <user_id>: Target user id

    Body (Required):
    None

    Body (Optional):
    'email'
    'password'

    Body (Not Allowed):
    None

    Success (200): Returns updated user

    Fail (40X):
    """
    try:
        user = User(get_request_data())
        user.id = user_id
        if user.password:
            user.password = encrypt(user.password)
        user.save()
    except (AttributeError, RequiredAttributes, EmailExists) as e:
        return Response(json.dumps({'error': str(e)}), status=400)
    return Response(json.dumps(user.serialize()), status=200)
