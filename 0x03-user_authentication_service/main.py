#!/usr/bin/env python3
"""main.py"""
import requests

BASE_URL = "http://localhost:5000"  # Adjust if your server is running on a different port

def register_user(email: str, password: str) -> None:
    """register user"""
    response = requests.post(f"{BASE_URL}/users", json={"email": email, "password": password})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.json() == {"email": email, "message": "user created"}, "Unexpected response payload"

def log_in_wrong_password(email: str, password: str) -> None:
    """login user"""
    response = requests.post(f"{BASE_URL}/sessions", json={"email": email, "password": password})
    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"

def log_in(email: str, password: str) -> str:
    """login user"""
    response = requests.post(f"{BASE_URL}/sessions", json={"email": email, "password": password})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "session_id" in response.cookies, "Session ID not found in cookies"
    return response.cookies.get("session_id")

def profile_unlogged() -> None:
    """profile when not logged in"""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Expected status code 403, got {response.status_code}"

def profile_logged(session_id: str) -> None:
    """profile when logged in"""
    response = requests.get(f"{BASE_URL}/profile", cookies={"session_id": session_id})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "email" in response.json(), "Email not found in response payload"

def log_out(session_id: str) -> None:
    """logout"""
    response = requests.delete(f"{BASE_URL}/sessions", cookies={"session_id": session_id})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def reset_password_token(email: str) -> str:
    """reseting password"""
    response = requests.post(f"{BASE_URL}/reset_password", json={"email": email})
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert "email" in response.json() and "reset_token" in response.json(), "Unexpected response payload"
    return response.json()["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """updating password"""
    response = requests.put(f"{BASE_URL}/reset_password", json={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.json() == {"email": email, "message": "Password updated"}, "Unexpected response payload"

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)