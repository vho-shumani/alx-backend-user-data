#!/usr/bin/env python3
"""Flask app"""
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, jsonify, request, abort, make_response, redirect, url_for
from auth import Auth


AUTH = Auth()
app = Flask(__name__)

@app.route('/')
def index():
    """home page"""
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'], strict_slashes=False)
def registration():
    """registers a new user"""
    email = request.form['email']
    password = request.form['password']
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    
@app.route('/sessions', methods=['POST'], strict_slashes=False)
def sessions_login():
    """Implements user login"""
    email = request.form['email']
    password = request.form['password']
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response

@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def sessions_logout():
    """Implement user logout"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for('/'))

@app.route('/profile', strict_slashes=False)
def profile():
    """Retrieves user profile"""
    session_id = request.cookies.get('session_id')

    if session_id is None:
        abort(403)
    
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
    
    return jsonify({"email": user.email}), 200

@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def reset_password():
    """resets password"""
    from db import DB
    db = DB()
    email = request.form['email']
    try:
        db.find_user_by(email=email)
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except NoResultFound:
        abort(403)

@app.route('reset_password', methods=["PUT"], strict_slashes=False)
def update_password():
    """updates password"""
    email = request.form['email']
    reset_token = request.form['reset_token']
    new_password = request.form['new_password']

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except NoResultFound:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
