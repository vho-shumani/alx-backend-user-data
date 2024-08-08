#!/usr/bin/env python3
"""Manage the Basic authentication
"""
from api.v1.auth.auth import Auth
import base64
import re


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
                                           base64_authorization_header: str) -> str:
        """"return the decoded value of a Base64 string"""
        if base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try: 
            return base64_authorization_header.decode('utf-8')
        except(UnicodeDecodeError, TypeError):
            return None
           
