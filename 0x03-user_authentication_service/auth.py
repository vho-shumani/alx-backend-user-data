#!/usr/bin/env python3
"""Authentication Module"""
import bcrypt
from db import DB
import logging
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from typing import Union, Optional


def _hash_password(password: str) -> bytes:
    """hashes password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """generates a uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_pass = _hash_password(password)
            user = self._db.add_user(email, hashed_pass)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """validates the login credentials"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Union[str, None]:
        """Create a session id for a user"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieves user using session_id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: str) -> None:
        """Destroys a session"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Updates user reset token"""
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError("user does not exist")

    def update_password(self, reset_token: str, password: str) -> None:
        """updates a user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
            return None
        except NoResultFound:
            raise ValueError("user doesnot exist.")
