#!/usr/bin/env python3
"""SessionDBAuth module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """Create and store a new UserSession and return the Session ID"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return the User ID by requesting UserSession in the database"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None

        user_session = user_sessions[0]
        created_at = user_session.created_at
        if self.session_duration <= 0:
            return user_session.user_id

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy the UserSession based on the Session ID from the request cookie"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        UserSession.load_from_file()
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        return True
