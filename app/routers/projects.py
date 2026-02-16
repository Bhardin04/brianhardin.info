from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.models.project import Project
from app.services.project import project_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


async def _get_all_projects() -> list[Project]:
    """Get all projects from DB or in-memory service."""
    if settings.USE_DATABASE:
        from app.database.connection import get_db
        from app.services.db_adapters import db_project_to_pydantic
        from app.services.project_db import project_service_db

        async for db in get_db():
            db_projects = await project_service_db.get_all(db)
            return [db_project_to_pydantic(p) for p in db_projects]
        return []
    return project_service.get_all()


async def _get_project_by_id(project_id: int) -> Project | None:
    """Get a single project by ID from DB or in-memory service."""
    if settings.USE_DATABASE:
        from app.database.connection import get_db
        from app.services.db_adapters import db_project_to_pydantic
        from app.services.project_db import project_service_db

        async for db in get_db():
            db_project = await project_service_db.get_by_id(db, project_id)
            if db_project:
                return db_project_to_pydantic(db_project)
            return None
        return None
    return project_service.get_by_id(project_id)


@router.get("/", response_class=HTMLResponse)
async def projects_list(request: Request) -> HTMLResponse:
    all_projects = await _get_all_projects()
    # Sort: featured first, then by creation date
    projects = sorted(
        all_projects,
        key=lambda p: (
            not p.featured,
            -(p.created_at.timestamp() if p.created_at else 0),
        ),
    )
    return templates.TemplateResponse(
        request, "projects.html", context={"projects": projects}
    )


@router.get("/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: int) -> HTMLResponse:
    project = await _get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get related projects (same category)
    all_projects = await _get_all_projects()
    related_projects = [
        p for p in all_projects if p.category == project.category and p.id != project_id
    ][:3]

    return templates.TemplateResponse(
        request,
        "project_detail.html",
        context={"project": project, "related_projects": related_projects},
    )
