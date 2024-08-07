#!/usr/bin/env python3
"""Manage the Basic authentication
"""
import re
from api.v1.auth.auth import Auth


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
