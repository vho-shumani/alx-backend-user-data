#!/usr/bin/env python3
"""Class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """Manages the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authenication is required"""
        if not path:
            return True

        if path[-1] != '/':
            path += '/'

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        for excluded_path in excluded_paths:
            excluded_path = excluded_path.rstrip('/')
            if excluded_path + '/' == path:
                return False
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header
        """
        if not request:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def session_cookie(self, request=None):
        """Retrieves the value of the cookie header"""
        if not request:
            return None
        cookie_name = os.getenv('SESSION_NAME')
        return request.cookies.get(cookie_name)

    def current_user(self, request=None) -> TypeVar('User'):
        """Handles current user
        """
        return None
