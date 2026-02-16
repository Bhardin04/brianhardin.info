"""Tests for CSRF protection and rate limiting."""

import time
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.middleware import (
    CSRF_COOKIE_NAME,
    CSRF_TOKEN_EXPIRY,
    generate_csrf_token,
    limiter,
    validate_csrf_token,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_limiter():
    """Reset rate limiter state between tests."""
    limiter._limiter.storage.reset()
    yield


# --- CSRF Token Utilities ---


class TestCSRFTokenUtilities:
    def test_token_format(self):
        token = generate_csrf_token()
        parts = token.split(".")
        assert len(parts) == 3, "Token must have 3 dot-separated parts"

    def test_valid_token_passes_validation(self):
        token = generate_csrf_token()
        assert validate_csrf_token(token) is True

    def test_tampered_signature_rejected(self):
        token = generate_csrf_token()
        parts = token.split(".")
        parts[2] = "a" * len(parts[2])  # replace signature
        tampered = ".".join(parts)
        assert validate_csrf_token(tampered) is False

    def test_tampered_random_rejected(self):
        token = generate_csrf_token()
        parts = token.split(".")
        parts[0] = "tampered"
        tampered = ".".join(parts)
        assert validate_csrf_token(tampered) is False

    def test_expired_token_rejected(self):
        token = generate_csrf_token()
        with patch("app.middleware.time") as mock_time:
            mock_time.time.return_value = time.time() + CSRF_TOKEN_EXPIRY + 1
            assert validate_csrf_token(token) is False

    def test_malformed_token_rejected(self):
        assert validate_csrf_token("not-a-valid-token") is False
        assert validate_csrf_token("") is False
        assert validate_csrf_token("a.b") is False
        assert validate_csrf_token("a.b.c.d") is False

    def test_non_numeric_timestamp_rejected(self):
        token = generate_csrf_token()
        parts = token.split(".")
        parts[1] = "notanumber"
        tampered = ".".join(parts)
        assert validate_csrf_token(tampered) is False


# --- CSRF Protection (HTTP) ---


class TestCSRFProtection:
    def test_contact_page_sets_csrf_cookie(self):
        response = client.get("/contact")
        assert response.status_code == 200
        assert CSRF_COOKIE_NAME in response.cookies

    def test_contact_page_has_hidden_input(self):
        response = client.get("/contact")
        assert 'name="csrf_token"' in response.text
        assert 'type="hidden"' in response.text

    def test_valid_csrf_token_accepted(self):
        token = generate_csrf_token()
        form_data = {
            "name": "Test",
            "email": "test@example.com",
            "subject": "Subject",
            "message": "Message",
            "csrf_token": token,
        }
        response = client.post(
            "/api/contact", data=form_data, cookies={"csrf_token": token}
        )
        assert response.status_code == 200

    def test_missing_csrf_token_rejected(self):
        form_data = {
            "name": "Test",
            "email": "test@example.com",
            "subject": "Subject",
            "message": "Message",
        }
        response = client.post("/api/contact", data=form_data)
        assert response.status_code == 403

    def test_mismatched_csrf_token_rejected(self):
        token1 = generate_csrf_token()
        token2 = generate_csrf_token()
        form_data = {
            "name": "Test",
            "email": "test@example.com",
            "subject": "Subject",
            "message": "Message",
            "csrf_token": token1,
        }
        response = client.post(
            "/api/contact", data=form_data, cookies={"csrf_token": token2}
        )
        assert response.status_code == 403

    def test_tampered_csrf_token_rejected(self):
        token = generate_csrf_token()
        parts = token.split(".")
        parts[2] = "a" * len(parts[2])
        tampered = ".".join(parts)
        form_data = {
            "name": "Test",
            "email": "test@example.com",
            "subject": "Subject",
            "message": "Message",
            "csrf_token": tampered,
        }
        response = client.post(
            "/api/contact", data=form_data, cookies={"csrf_token": tampered}
        )
        assert response.status_code == 403

    def test_csrf_error_returns_friendly_html(self):
        form_data = {
            "name": "Test",
            "email": "test@example.com",
            "subject": "Subject",
            "message": "Message",
        }
        response = client.post("/api/contact", data=form_data)
        assert response.status_code == 403
        assert "reload" in response.text.lower() or "session" in response.text.lower()


# --- Rate Limiting ---


class TestRateLimiting:
    def test_contact_form_rate_limited(self):
        """Contact form should be rate limited to 1/minute."""
        token = generate_csrf_token()
        form_data = {
            "name": "Test",
            "email": "test@example.com",
            "subject": "Subject",
            "message": "Message",
            "csrf_token": token,
        }
        # First request should succeed
        response = client.post(
            "/api/contact", data=form_data, cookies={"csrf_token": token}
        )
        assert response.status_code == 200

        # Second request within the same minute should be rate limited
        token2 = generate_csrf_token()
        form_data["csrf_token"] = token2
        response = client.post(
            "/api/contact", data=form_data, cookies={"csrf_token": token2}
        )
        assert response.status_code == 429

    def test_analytics_rate_limited(self):
        """Analytics endpoint should be rate limited to 30/minute."""
        for i in range(31):
            response = client.post("/api/analytics", json={"event": f"test_{i}"})
            if response.status_code == 429:
                assert i >= 30, "Rate limit hit too early"
                return
        pytest.fail("Rate limit was never triggered after 31 requests")

    def test_demo_session_rate_limited(self):
        """Demo session creation should be rate limited to 10/minute."""
        for i in range(11):
            response = client.post("/demos/api/payment-processing/session")
            if response.status_code == 429:
                assert i >= 10, "Rate limit hit too early"
                return
        pytest.fail("Rate limit was never triggered after 11 requests")

    def test_rate_limit_returns_429(self):
        """Rate limit responses return 429 status code."""
        token = generate_csrf_token()
        form_data = {
            "name": "Test",
            "email": "test@example.com",
            "subject": "Subject",
            "message": "Message",
            "csrf_token": token,
        }
        client.post("/api/contact", data=form_data, cookies={"csrf_token": token})
        token2 = generate_csrf_token()
        form_data["csrf_token"] = token2
        response = client.post(
            "/api/contact", data=form_data, cookies={"csrf_token": token2}
        )
        assert response.status_code == 429
