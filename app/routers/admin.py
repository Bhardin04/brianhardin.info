"""Admin panel routes."""

import logging

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from starlette.responses import Response

from app.admin.dependencies import require_admin
from app.database.connection import get_db
from app.database.models import AdminSession, BlogPost, ContactMessage, Project

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """Admin dashboard with stats and recent messages."""
    blog_count = 0
    project_count = 0
    unread_count = 0
    recent_messages: list[ContactMessage] = []

    async for db in get_db():
        blog_result = await db.execute(select(func.count(BlogPost.id)))
        blog_count = blog_result.scalar() or 0

        project_result = await db.execute(select(func.count(Project.id)))
        project_count = project_result.scalar() or 0

        unread_result = await db.execute(
            select(func.count(ContactMessage.id)).where(
                ContactMessage.read == False,  # noqa: E712
                ContactMessage.archived == False,  # noqa: E712
            )
        )
        unread_count = unread_result.scalar() or 0

        messages_result = await db.execute(
            select(ContactMessage)
            .where(ContactMessage.archived == False)  # noqa: E712
            .order_by(ContactMessage.created_at.desc())
            .limit(5)
        )
        recent_messages = list(messages_result.scalars().all())

    return templates.TemplateResponse(
        request,
        "admin/dashboard.html",
        context={
            "admin_user": session.github_username,
            "blog_count": blog_count,
            "project_count": project_count,
            "unread_count": unread_count,
            "recent_messages": recent_messages,
        },
    )
