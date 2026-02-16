import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.middleware import generate_csrf_token, limiter

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_limiter():
    """Reset rate limiter state between tests."""
    limiter._limiter.storage.reset()
    yield


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "Brian Hardin" in response.text


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_projects_page():
    response = client.get("/projects")
    assert response.status_code == 200


def test_api_projects():
    response = client.get("/api/projects")
    assert response.status_code == 200
    projects = response.json()
    assert isinstance(projects, list)
    assert len(projects) > 0


def test_about_page():
    response = client.get("/about")
    assert response.status_code == 200
    assert "About Me" in response.text


def test_contact_page():
    response = client.get("/contact")
    assert response.status_code == 200
    assert "Get In Touch" in response.text


def test_resume_page():
    response = client.get("/resume")
    assert response.status_code == 200
    assert "Resume" in response.text


def test_project_detail():
    response = client.get("/projects/3")
    assert response.status_code == 200


def test_contact_form_submission():
    token = generate_csrf_token()
    form_data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message",
        "company": "Test Company",
        "csrf_token": token,
    }
    response = client.post(
        "/api/contact", data=form_data, cookies={"csrf_token": token}
    )
    assert response.status_code == 200
    assert "Success!" in response.text


def test_contact_form_missing_fields():
    token = generate_csrf_token()
    form_data = {
        "name": "Test User",
        "csrf_token": token,
        # Missing required fields
    }
    response = client.post(
        "/api/contact", data=form_data, cookies={"csrf_token": token}
    )
    assert response.status_code == 422  # Validation error
