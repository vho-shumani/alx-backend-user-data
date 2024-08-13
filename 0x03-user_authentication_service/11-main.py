#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth
import bcrypt

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

user = auth.register_user(email, password)
token = auth.get_reset_password_token(email)
