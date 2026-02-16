from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.services.project import project_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def projects_list(request: Request) -> HTMLResponse:
    projects = project_service.get_sorted()
    return templates.TemplateResponse(
        request, "projects.html", context={"projects": projects}
    )


@router.get("/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: int) -> HTMLResponse:
    project = project_service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    related_projects = project_service.get_related(project_id)

    return templates.TemplateResponse(
        request,
        "project_detail.html",
        context={"project": project, "related_projects": related_projects},
    )
