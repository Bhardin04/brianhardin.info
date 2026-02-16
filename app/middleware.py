"""Security middleware: rate limiting and CSRF protection."""

import hashlib
import hmac
import secrets
import time

from fastapi import Cookie, Form, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

# --- Rate Limiter ---

limiter = Limiter(key_func=get_remote_address)

# --- CSRF Protection (Double Submit Cookie) ---

CSRF_COOKIE_NAME = "csrf_token"
CSRF_FIELD_NAME = "csrf_token"
CSRF_TOKEN_EXPIRY = 3600  # 1 hour


def generate_csrf_token() -> str:
    """Create a signed CSRF token: {random}.{timestamp}.{signature}."""
    random_part = secrets.token_urlsafe(32)
    timestamp = str(int(time.time()))
    payload = f"{random_part}.{timestamp}"
    signature = hmac.new(
        settings.SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}.{signature}"


def validate_csrf_token(token: str) -> bool:
    """Verify signature and check expiry on a CSRF token."""
    parts = token.split(".")
    if len(parts) != 3:
        return False

    random_part, timestamp_str, signature = parts

    # Verify signature
    payload = f"{random_part}.{timestamp_str}"
    expected_signature = hmac.new(
        settings.SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(signature, expected_signature):
        return False

    # Check expiry
    try:
        token_time = int(timestamp_str)
    except ValueError:
        return False

    if time.time() - token_time > CSRF_TOKEN_EXPIRY:
        return False

    return True


async def verify_csrf_token(
    request: Request,
    csrf_token: str = Form(None),
    csrf_cookie: str | None = Cookie(None, alias=CSRF_COOKIE_NAME),
) -> None:
    """FastAPI dependency: validate Double Submit Cookie CSRF protection."""
    if not csrf_token or not csrf_cookie:
        raise HTTPException(status_code=403, detail="Missing CSRF token")

    if csrf_token != csrf_cookie:
        raise HTTPException(status_code=403, detail="CSRF token mismatch")

    if not validate_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid or expired CSRF token")
