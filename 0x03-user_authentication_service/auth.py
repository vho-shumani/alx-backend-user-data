#!/usr/bin/env python3
"""Module takes in a password string arguments and returns bytes"""
import bcrypt
from db import DB
import logging
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """hashes password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


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
            pass
        hashed_pass = self._hash_password(password)
        return self._db.add_user(email, hashed_pass)

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

    def _generate_uuid(self) -> str:
        """generates a uuid"""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a session id for a user"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieves user using session_id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Destroys a session"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Updates user reset token"""
        try:
            user = self._db.find_user_by(email=email)
            token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError("user does not exist")

    def update_password(self, reset_token: str, password: str) -> None:
        """updates a user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = self._hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
            return None
        except NoResultFound:
            raise ValueError("user doesnot exist.")
