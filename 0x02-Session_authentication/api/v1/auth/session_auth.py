#!/usr/bin/env python3
"""Module contain session authorization class"""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session authorzation"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for a user_id"""
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrieves user id based on session id"""
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(f'{session_id}')

    def current_user(self, request=None):
        """Retrieves User based on cookie value"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(id=user_id)

    def destroy_session(self, request=None):
        """Deletes a user session/logout"""
        if not request:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
