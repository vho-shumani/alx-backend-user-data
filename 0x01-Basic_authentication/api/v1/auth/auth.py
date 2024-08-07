#!/usr/bin/python3
"""Class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """Manages the API authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """"""
        if path and path[-1] != '/':
            path += '/'
        if not path or not excluded_paths:
            return True
        if path not in excluded_paths or len(excluded_paths) == 0:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        """
        if not request:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """"""
        return None
