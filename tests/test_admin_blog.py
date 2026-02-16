"""Tests for admin blog CRUD operations."""

import json
import secrets
from datetime import UTC, datetime, timedelta

import pytest
from starlette.testclient import TestClient

from app.database.connection import get_db, init_db
from app.database.models import AdminSession, BlogPost
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
async def sample_post():
    """Create a sample blog post in the database."""
    async for db in get_db():
        post = BlogPost(
            title="Test Post",
            slug="test-post",
            content="# Hello\n\nThis is a test post.",
            content_html="<h1>Hello</h1><p>This is a test post.</p>",
            excerpt="A test post",
            tags=json.dumps(["Python", "Testing"]),
            published=True,
            featured=False,
            author="Brian Hardin",
            meta_description="Test post description",
            reading_time_minutes=1,
        )
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post
    return None


class TestBlogList:
    def test_blog_list_requires_auth(self):
        client = TestClient(app, follow_redirects=False)
        response = client.get("/admin/blog")
        # 401 for non-HTML requests (test client doesn't send Accept: text/html)
        assert response.status_code == 401

    def test_blog_list_empty(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/blog")
        assert response.status_code == 200
        assert "No blog posts yet" in response.text

    def test_blog_list_with_posts(self, admin_session, sample_post):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/blog")
        assert response.status_code == 200
        assert "Test Post" in response.text
        assert "Published" in response.text


class TestBlogCreate:
    def test_new_post_form(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/blog/new")
        assert response.status_code == 200
        assert "New Post" in response.text
        assert "csrf_token" in response.text

    def test_create_post(self, admin_session):
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("admin_session", admin_session)

        # Get CSRF token
        csrf = generate_csrf_token()
        client.cookies.set("csrf_token", csrf)

        response = client.post(
            "/admin/blog/new",
            data={
                "title": "My New Post",
                "slug": "my-new-post",
                "content": "# Hello World\n\nThis is content.",
                "excerpt": "A new post",
                "tags": "Python, FastAPI",
                "published": "true",
                "featured": "",
                "author": "Brian Hardin",
                "meta_description": "A new post about things",
                "csrf_token": csrf,
            },
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/admin/blog"


class TestBlogEdit:
    def test_edit_form_loads(self, admin_session, sample_post):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get(f"/admin/blog/{sample_post.id}/edit")
        assert response.status_code == 200
        assert "Test Post" in response.text
        assert "Edit Post" in response.text

    def test_edit_form_not_found(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/blog/999/edit")
        assert response.status_code == 404

    def test_update_post(self, admin_session, sample_post):
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("admin_session", admin_session)

        csrf = generate_csrf_token()
        client.cookies.set("csrf_token", csrf)

        response = client.post(
            f"/admin/blog/{sample_post.id}/edit",
            data={
                "title": "Updated Title",
                "slug": "updated-title",
                "content": "Updated content here.",
                "excerpt": "Updated excerpt",
                "tags": "Updated",
                "published": "true",
                "featured": "true",
                "author": "Brian Hardin",
                "meta_description": "Updated description",
                "csrf_token": csrf,
            },
        )
        assert response.status_code == 302


class TestBlogDelete:
    def test_delete_post(self, admin_session, sample_post):
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("admin_session", admin_session)
        response = client.post(f"/admin/blog/{sample_post.id}/delete")
        assert response.status_code == 302

        # Verify post is gone
        client2 = TestClient(app)
        client2.cookies.set("admin_session", admin_session)
        response = client2.get("/admin/blog")
        assert "Test Post" not in response.text

    def test_delete_not_found(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.post("/admin/blog/999/delete")
        assert response.status_code == 404


class TestBlogPublishToggle:
    def test_toggle_publish(self, admin_session, sample_post):
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("admin_session", admin_session)
        # sample_post is published=True, toggling should unpublish
        response = client.post(f"/admin/blog/{sample_post.id}/publish")
        assert response.status_code == 302

    def test_toggle_not_found(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.post("/admin/blog/999/publish")
        assert response.status_code == 404
