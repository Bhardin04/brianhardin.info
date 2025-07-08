from fastapi import APIRouter
from app.models.project import Project

router = APIRouter()

@router.get("/projects")
async def get_projects():
    return [
        Project(
            id=1,
            title="Personal Website",
            description="FastAPI-based personal brand website",
            technologies=["Python", "FastAPI", "Jinja2", "HTMX"],
            github_url="https://github.com/Bhardin04/brianhardin.info",
            demo_url="https://brianhardin.info"
        )
    ]

@router.get("/projects/{project_id}")
async def get_project(project_id: int):
    return Project(
        id=project_id,
        title="Project Details",
        description="Detailed view of the project",
        technologies=["Python", "FastAPI"],
        github_url="https://github.com/example",
        demo_url="https://example.com"
    )