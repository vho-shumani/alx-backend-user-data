#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.auth.session_db_auth import SessionDBAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
AUTH_TYPE = os.getenv('AUTH_TYPE')

if AUTH_TYPE:
    if AUTH_TYPE == 'basic_auth':
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif AUTH_TYPE == 'session_auth':
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.errorhandler(403)
def forbidden(error) -> str:
    """forbidden error handler"""
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def unauthorized(error) -> str:
    """unauthorized handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.before_request
def before_request():
    """run before each request
    """

    if auth:
        excluded_paths = ['/api/v1/status/',
                          '/api/v1/unauthorized/',
                          '/api/v1/forbidden/',
                          '/api/v1/auth_session/login/'
                          ]
        if not auth.require_auth(request.path, excluded_paths):
            return

        if (not auth.authorization_header(request) and
                not auth.session_cookie(request)):
            abort(401)

        request.current_user = auth.current_user(request)
        if auth.current_user(request) is None:
            abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    auth_type = getenv("AUTH_TYPE")
    
    if auth_type == "session_auth":
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    elif auth_type == "session_exp_auth":
        from api.v1.auth.session_exp_auth import SessionExpAuth
        auth = SessionExpAuth()
    elif auth_type == "session_db_auth":
        auth = SessionDBAuth()
    elif auth_type == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()
    
    app.run(host=host, port=port)
