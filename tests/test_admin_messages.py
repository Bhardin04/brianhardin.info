"""Tests for admin messages and settings."""

import secrets
from datetime import UTC, datetime, timedelta

import pytest
from starlette.testclient import TestClient

from app.database.connection import get_db, init_db
from app.database.models import AdminSession, ContactMessage
from app.main import app
from app.middleware import generate_csrf_token


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
    """Create a valid admin session."""
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


@pytest.fixture
async def sample_message():
    """Create a sample contact message."""
    async for db in get_db():
        msg = ContactMessage(
            name="John Doe",
            email="john@example.com",
            subject="Test Subject",
            message="Hello, this is a test message.",
            company="Test Corp",
        )
        db.add(msg)
        await db.commit()
        await db.flush()
        return msg
    return None


class TestMessageList:
    def test_messages_requires_auth(self):
        client = TestClient(app, follow_redirects=False)
        response = client.get("/admin/messages")
        assert response.status_code == 401

    def test_messages_empty(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/messages")
        assert response.status_code == 200
        assert "No messages yet" in response.text

    def test_messages_with_message(self, admin_session, sample_message):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/messages")
        assert response.status_code == 200
        assert "John Doe" in response.text
        assert "Test Subject" in response.text


class TestMessageDetail:
    def test_view_message(self, admin_session, sample_message):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get(f"/admin/messages/{sample_message.id}")
        assert response.status_code == 200
        assert "John Doe" in response.text
        assert "Hello, this is a test message." in response.text

    def test_view_not_found(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/messages/999")
        assert response.status_code == 404


class TestMessageArchive:
    def test_archive_message(self, admin_session, sample_message):
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("admin_session", admin_session)
        response = client.post(f"/admin/messages/{sample_message.id}/archive")
        assert response.status_code == 302

    def test_archive_not_found(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.post("/admin/messages/999/archive")
        assert response.status_code == 404


class TestMessageDelete:
    def test_delete_message(self, admin_session, sample_message):
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("admin_session", admin_session)
        response = client.post(f"/admin/messages/{sample_message.id}/delete")
        assert response.status_code == 302

    def test_delete_not_found(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.post("/admin/messages/999/delete")
        assert response.status_code == 404


class TestSettings:
    def test_settings_requires_auth(self):
        client = TestClient(app, follow_redirects=False)
        response = client.get("/admin/settings")
        assert response.status_code == 401

    def test_settings_page_loads(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/settings")
        assert response.status_code == 200
        assert "Site Settings" in response.text
        assert "csrf_token" in response.text

    def test_save_settings(self, admin_session):
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("admin_session", admin_session)

        csrf = generate_csrf_token()
        client.cookies.set("csrf_token", csrf)

        response = client.post(
            "/admin/settings",
            data={
                "site_title": "My Site",
                "site_description": "A test site",
                "contact_email": "test@example.com",
                "github_url": "https://github.com/test",
                "linkedin_url": "",
                "twitter_url": "",
                "csrf_token": csrf,
            },
        )
        assert response.status_code == 302
        assert "saved=true" in response.headers["location"]
