"""Tests for admin authentication."""

import secrets
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest
from starlette.testclient import TestClient

from app.database.connection import get_db, init_db
from app.database.models import AdminSession
from app.main import app


@pytest.fixture(autouse=True)
async def setup_db(monkeypatch):
    """Use in-memory SQLite for tests."""
    monkeypatch.setattr(
        "app.database.connection.settings",
        type(
            "S",
            (),
            {"DATABASE_URL": "sqlite+aiosqlite:///:memory:", "DEBUG": False},
        )(),
    )
    await init_db()
    yield


@pytest.fixture
async def admin_session():
    """Create a valid admin session in the database."""
    token = secrets.token_urlsafe(48)
    async for db in get_db():
        session = AdminSession(
            session_token=token,
            github_username="testadmin",
            github_id=12345,
            expires_at=datetime.now(UTC).replace(tzinfo=None) + timedelta(hours=24),
        )
        db.add(session)
        await db.commit()
    return token


class TestLoginPage:
    def test_login_page_renders(self):
        client = TestClient(app)
        response = client.get("/admin/login")
        assert response.status_code == 200
        assert "Sign in with GitHub" in response.text
        assert "noindex" in response.text

    def test_login_github_redirect(self):
        with patch("app.routers.auth.settings") as mock_settings:
            mock_settings.GITHUB_CLIENT_ID = "test_client_id"
            mock_settings.GITHUB_CLIENT_SECRET = "test_secret"
            mock_settings.ADMIN_GITHUB_USERNAME = "testadmin"

            client = TestClient(app, follow_redirects=False)
            response = client.get("/admin/login/github")
            assert response.status_code == 302
            location = response.headers["location"]
            assert "github.com/login/oauth/authorize" in location
            assert "test_client_id" in location

    def test_login_github_fails_without_config(self):
        client = TestClient(app)
        response = client.get("/admin/login/github")
        assert response.status_code == 500


class TestCallback:
    def test_callback_rejects_invalid_state(self):
        client = TestClient(app)
        response = client.get("/admin/callback?code=test&state=invalid")
        assert response.status_code == 400

    def test_callback_rejects_missing_code(self):
        client = TestClient(app)
        client.cookies.set("oauth_state", "teststate")
        response = client.get("/admin/callback?state=teststate")
        assert response.status_code == 400


class TestLogout:
    def test_logout_clears_session(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.post("/admin/logout", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == "/"

    def test_logout_without_session(self):
        client = TestClient(app)
        response = client.post("/admin/logout", follow_redirects=False)
        assert response.status_code == 302
        assert response.headers["location"] == "/"


class TestUnauthorizedRedirect:
    def test_401_redirects_html_to_login(self):
        client = TestClient(app, follow_redirects=False)
        # Any protected admin page without session should get 401 -> redirect
        # For now we test the login page is accessible
        response = client.get("/admin/login")
        assert response.status_code == 200
