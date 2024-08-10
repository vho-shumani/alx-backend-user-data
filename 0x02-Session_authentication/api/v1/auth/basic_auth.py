#!/usr/bin/env python3
"""Manage the Basic authentication
"""
from api.v1.auth.auth import Auth
import base64
import re
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Impletment Basic authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if authorization_header[:6] != "Basic ":
            return None
        else:
            return re.split("Basic ", authorization_header)[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """"return the decoded value of a Base64 string"""
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded = base64.b64decode(encoded)
            return decoded.decode('utf-8')
        except BaseException:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Extracts the user email and password"""
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        email = decoded_base64_authorization_header.split(':')[0]
        password = ":".join(decoded_base64_authorization_header.split(':')[1:])
        return (email, password)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """Return the User instance based in his email and password"""
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        if not users:
            return None

        if not users[0].is_valid_password(user_pwd):
            return None
        else:
            return users[0]

    def current_user(self,
                     request=None
                     ) -> TypeVar('User'):
        """Retrieves the user instance for a request"""
        if not request:
            return None

        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        base64_auth = self.extract_base64_authorization_header(auth_header)
        if not base64_auth:
            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if not decoded_auth:
            return None

        user_email, password = self.extract_user_credentials(decoded_auth)
        if not user_email or not password:
            return None

        return self.user_object_from_credentials(user_email, password)
