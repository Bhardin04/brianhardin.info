from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from app.models.project import Project

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def projects_list(request: Request) -> Response:
    projects = [
        Project(
            id=1,
            title="Personal Website",
            description="FastAPI-based personal brand website",
            technologies=["Python", "FastAPI", "Jinja2", "HTMX"],
            github_url="https://github.com/Bhardin04/brianhardin.info",
            demo_url="https://brianhardin.info",
        )
    ]
    return templates.TemplateResponse(
        "projects.html", {"request": request, "projects": projects}
    )


@router.get("/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: int) -> Response:
    project = Project(
        id=project_id,
        title="Project Details",
        description="Detailed view of the project",
        technologies=["Python", "FastAPI"],
        github_url="https://github.com/example",
        demo_url="https://example.com",
    )
    return templates.TemplateResponse(
        "project_detail.html", {"request": request, "project": project}
    )
