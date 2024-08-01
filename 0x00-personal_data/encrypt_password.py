#!/usr/bin/env python3
"""encrypt_password.py"""
import bcrypt


def hash_password(password: str) -> str:
    """returns a salted, hashed password"""
    password_byte = str.encode(password)
    return bcrypt.hashpw(password_byte, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password matches the hashed password"""
    if bcrypt.checkpw(str.encode(password), hashed_password):
        return True
    return False
