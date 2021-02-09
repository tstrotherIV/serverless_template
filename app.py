import json
import logging
import traceback
from api.sessions import sessions_bp
from api.users import users_bp
from constants.error_constants import ErrorConstants
from flask import Flask, request, Response, g
from security.generic import is_allowed_by_all

# configure default logger
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# disable 3rd party logging
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('requests').setLevel(logging.CRITICAL)


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    register_index(app)
    register_blueprints(app)
    register_before_request_handler(app)
    register_after_request_handler(app)
    register_error_handlers(app)
    return app


def register_index(app):
    @app.route("/", methods=['GET'])
    @is_allowed_by_all
    def index():
        return Response(json.dumps({'message': 'success'}), status=200)


def register_blueprints(app):
    app.register_blueprint(sessions_bp)
    app.register_blueprint(users_bp)


def register_before_request_handler(app):
    def before_request_handler():
        logger.debug('########## Request Received ########################################')
        logger.debug({'method': request.method})
        logger.debug({'url': request.url})
        logger.debug({'headers': request.headers})
        logger.debug({'body': request.data})

    app.before_request(before_request_handler)


def register_after_request_handler(app):
    def after_request_handler(response):
        if not g.get('authenticated') and int(response.status_code) < 400:
            response = Response(json.dumps({'error': ErrorConstants.App.UNABLE_TO_AUTHENTICATE}), status=401)

        response.headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,X-Api-Key,X-Amz-Security-Token,Authorization,session_id"
        }

        logger.debug('########## Response Sent ########################################')
        logger.debug({'status': response.status})
        logger.debug({'headers': response.headers})
        logger.debug({'body': response.response})

        return response

    app.after_request(after_request_handler)


def register_error_handlers(app):
    from werkzeug.exceptions import NotFound, MethodNotAllowed

    def not_found_error(e):
        logger.critical('########## Not Found Error ########################################')
        logger.critical("{}: {}".format(e.__class__.__name__, e))
        logger.critical(traceback.format_exc())
        return Response(json.dumps({'error': ErrorConstants.App.REQUESTED_URL_NOT_FOUND}), status=404)
    app.register_error_handler(NotFound, not_found_error)

    def method_not_allowed_error(e):
        logger.critical('########## Method Not Allowed Error ########################################')
        logger.critical("{}: {}".format(e.__class__.__name__, e))
        logger.critical(traceback.format_exc())
        return Response(json.dumps({'error': ErrorConstants.App.METHOD_NOT_ALLOWED}), status=405)
    app.register_error_handler(MethodNotAllowed, method_not_allowed_error)

    def internal_server_error(e):
        logger.critical('########## Internal Server Error ########################################')
        logger.critical("{}: {}".format(e.__class__.__name__, e))
        logger.critical(traceback.format_exc())
        return Response(json.dumps({'error': ErrorConstants.App.INTERNAL_SERVER_ERROR}), status=500)
    app.register_error_handler(Exception, internal_server_error)


app = create_app()
