"""Tests for admin project CRUD operations."""

import json
import secrets
from datetime import UTC, datetime, timedelta

import pytest
from starlette.testclient import TestClient

from app.database.connection import get_db, init_db
from app.database.models import AdminSession, Project
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
async def sample_project():
    """Create a sample project in the database."""
    async for db in get_db():
        project = Project(
            title="Test Project",
            description="A test project for testing.",
            long_description="This is a longer description.",
            technologies=json.dumps(["Python", "FastAPI"]),
            category="web_app",
            status="completed",
            featured=True,
            sort_order=1,
            image_url="",
            github_url="https://github.com/test/project",
            demo_url="https://demo.test.com",
            duration="5 weeks",
            role="Full-stack Developer",
            team_size="Solo developer",
            client_type="Startup",
            features=json.dumps(["Feature 1", "Feature 2"]),
            challenges=json.dumps(["Challenge 1"]),
            problem_json=json.dumps({"title": "Test Problem", "description": "Desc"}),
            solution_json=json.dumps({"approach": "Test approach"}),
            outcome_json=json.dumps({"summary": "Good outcome"}),
            timeline_json=json.dumps([{"phase": "Phase 1", "duration": "1 week"}]),
        )
        db.add(project)
        await db.commit()
        await db.flush()
        return project
    return None


class TestProjectList:
    def test_project_list_requires_auth(self):
        client = TestClient(app, follow_redirects=False)
        response = client.get("/admin/projects")
        assert response.status_code == 401

    def test_project_list_empty(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/projects")
        assert response.status_code == 200
        assert "No projects yet" in response.text

    def test_project_list_with_projects(self, admin_session, sample_project):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/projects")
        assert response.status_code == 200
        assert "Test Project" in response.text
        assert "web_app" in response.text


class TestProjectCreate:
    def test_new_project_form(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/projects/new")
        assert response.status_code == 200
        assert "New Project" in response.text
        assert "csrf_token" in response.text

    def test_create_project(self, admin_session):
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("admin_session", admin_session)

        csrf = generate_csrf_token()
        client.cookies.set("csrf_token", csrf)

        response = client.post(
            "/admin/projects/new",
            data={
                "title": "My New Project",
                "description": "A brand new project",
                "long_description": "Longer description here",
                "technologies": "Python, Docker",
                "category": "api",
                "status": "in_progress",
                "featured": "true",
                "sort_order": "1",
                "image_url": "",
                "github_url": "https://github.com/test",
                "demo_url": "",
                "duration": "3 weeks",
                "role": "Backend Developer",
                "team_size": "2 developers",
                "client_type": "Enterprise",
                "features": "Feature A\nFeature B",
                "challenges": "Challenge A",
                "csrf_token": csrf,
            },
        )
        assert response.status_code == 302
        assert response.headers["location"] == "/admin/projects"


class TestProjectEdit:
    def test_edit_form_loads(self, admin_session, sample_project):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get(f"/admin/projects/{sample_project.id}/edit")
        assert response.status_code == 200
        assert "Test Project" in response.text
        assert "Edit Project" in response.text

    def test_edit_form_not_found(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/projects/999/edit")
        assert response.status_code == 404

    def test_update_project(self, admin_session, sample_project):
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("admin_session", admin_session)

        csrf = generate_csrf_token()
        client.cookies.set("csrf_token", csrf)

        response = client.post(
            f"/admin/projects/{sample_project.id}/edit",
            data={
                "title": "Updated Project",
                "description": "Updated description",
                "long_description": "",
                "technologies": "React, Node.js",
                "category": "web_app",
                "status": "completed",
                "featured": "",
                "sort_order": "2",
                "image_url": "",
                "github_url": "",
                "demo_url": "",
                "duration": "",
                "role": "",
                "team_size": "",
                "client_type": "",
                "features": "",
                "challenges": "",
                "csrf_token": csrf,
            },
        )
        assert response.status_code == 302


class TestProjectDelete:
    def test_delete_project(self, admin_session, sample_project):
        client = TestClient(app, follow_redirects=False)
        client.cookies.set("admin_session", admin_session)
        response = client.post(f"/admin/projects/{sample_project.id}/delete")
        assert response.status_code == 302

        # Verify project is gone
        client2 = TestClient(app)
        client2.cookies.set("admin_session", admin_session)
        response = client2.get("/admin/projects")
        assert "Test Project" not in response.text

    def test_delete_not_found(self, admin_session):
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.post("/admin/projects/999/delete")
        assert response.status_code == 404


class TestProjectJsonRoundtrip:
    def test_technologies_roundtrip(self, admin_session, sample_project):
        """Verify technologies render correctly in the list."""
        client = TestClient(app)
        client.cookies.set("admin_session", admin_session)
        response = client.get("/admin/projects")
        assert response.status_code == 200
        assert "Python" in response.text
        assert "FastAPI" in response.text
