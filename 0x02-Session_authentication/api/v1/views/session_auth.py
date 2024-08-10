#!/usr/bin/env python3
""" Module of session authentication views
"""
from models.user import User
from flask import jsonify, abort
from api.v1.views import app_views
from flask import request
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """POST /auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or email == '':
        return jsonify({"error": "email missing"}), 400
    
    if not password or password == '':
        return jsonify({"error": "password missing"}), 400
    
    users = User.search({"email": email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password" }), 401
    
    from api.v1.app import auth
    session_id = auth.create_session(users[0].id)
    response = jsonify(users[0].to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response
