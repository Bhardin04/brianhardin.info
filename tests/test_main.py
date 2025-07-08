from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

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