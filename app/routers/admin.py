"""Admin panel routes."""

import json
import logging

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from starlette.responses import Response

from app.admin.dependencies import require_admin
from app.database.connection import get_db
from app.database.models import AdminSession, BlogPost, ContactMessage, Project
from app.middleware import generate_csrf_token, validate_csrf_token
from app.services.blog_db import blog_service_db, generate_slug

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")


def _parse_tags(tags_str: str) -> list[str]:
    """Parse comma-separated tags string into a list."""
    if not tags_str.strip():
        return []
    return [t.strip() for t in tags_str.split(",") if t.strip()]


def _tags_list_from_json(tags_json: str) -> list[str]:
    """Parse JSON tags string into a list (for template rendering)."""
    try:
        return json.loads(tags_json)  # type: ignore[no-any-return]
    except (json.JSONDecodeError, TypeError):
        return []


# ---------- Dashboard ----------


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


# ---------- Blog CRUD ----------


@router.get("/blog", response_class=HTMLResponse)
async def blog_list(
    request: Request,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """List all blog posts."""
    posts: list[BlogPost] = []
    async for db in get_db():
        posts = await blog_service_db.get_all(db)

    # Attach parsed tags as an attribute for template rendering
    for post in posts:
        post.tags_list = _tags_list_from_json(post.tags)  # type: ignore[attr-defined]

    return templates.TemplateResponse(
        request,
        "admin/blog/list.html",
        context={
            "admin_user": session.github_username,
            "posts": posts,
        },
    )


@router.get("/blog/new", response_class=HTMLResponse)
async def blog_new_form(
    request: Request,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """New blog post form."""
    csrf = generate_csrf_token()
    response = templates.TemplateResponse(
        request,
        "admin/blog/edit.html",
        context={
            "admin_user": session.github_username,
            "post": None,
            "csrf_token": csrf,
        },
    )
    response.set_cookie("csrf_token", csrf, httponly=True, samesite="strict")
    return response


@router.post("/blog/new")
async def blog_create(
    request: Request,
    session: AdminSession = Depends(require_admin),
    title: str = Form(...),
    slug: str = Form(""),
    content: str = Form(...),
    excerpt: str = Form(""),
    tags: str = Form(""),
    published: str = Form(""),
    featured: str = Form(""),
    author: str = Form("Brian Hardin"),
    meta_description: str = Form(""),
    csrf_token: str = Form(...),
) -> Response:
    """Create a new blog post."""
    cookie_csrf = request.cookies.get("csrf_token", "")
    if csrf_token != cookie_csrf or not validate_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    async for db in get_db():
        await blog_service_db.create(
            db,
            title=title,
            slug=slug or generate_slug(title),
            content=content,
            excerpt=excerpt,
            tags=_parse_tags(tags),
            published=published == "true",
            featured=featured == "true",
            author=author,
            meta_description=meta_description,
        )

    return RedirectResponse(url="/admin/blog", status_code=302)


@router.get("/blog/{post_id}/edit", response_class=HTMLResponse)
async def blog_edit_form(
    request: Request,
    post_id: int,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """Edit blog post form."""
    async for db in get_db():
        post = await blog_service_db.get_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        post.tags_list = _tags_list_from_json(post.tags)  # type: ignore[attr-defined]

        csrf = generate_csrf_token()
        response = templates.TemplateResponse(
            request,
            "admin/blog/edit.html",
            context={
                "admin_user": session.github_username,
                "post": post,
                "csrf_token": csrf,
            },
        )
        response.set_cookie("csrf_token", csrf, httponly=True, samesite="strict")
        return response

    raise HTTPException(status_code=500, detail="Database unavailable")


@router.post("/blog/{post_id}/edit")
async def blog_update(
    request: Request,
    post_id: int,
    session: AdminSession = Depends(require_admin),
    title: str = Form(...),
    slug: str = Form(""),
    content: str = Form(...),
    excerpt: str = Form(""),
    tags: str = Form(""),
    published: str = Form(""),
    featured: str = Form(""),
    author: str = Form("Brian Hardin"),
    meta_description: str = Form(""),
    csrf_token: str = Form(...),
) -> Response:
    """Update an existing blog post."""
    cookie_csrf = request.cookies.get("csrf_token", "")
    if csrf_token != cookie_csrf or not validate_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    async for db in get_db():
        post = await blog_service_db.get_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        await blog_service_db.update(
            db,
            post,
            title=title,
            slug=slug or generate_slug(title),
            content=content,
            excerpt=excerpt,
            tags=_parse_tags(tags),
            published=published == "true",
            featured=featured == "true",
            author=author,
            meta_description=meta_description,
        )

    return RedirectResponse(url="/admin/blog", status_code=302)


@router.post("/blog/{post_id}/delete")
async def blog_delete(
    request: Request,
    post_id: int,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """Delete a blog post."""
    async for db in get_db():
        post = await blog_service_db.get_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        await blog_service_db.delete(db, post)

    return RedirectResponse(url="/admin/blog", status_code=302)


@router.post("/blog/{post_id}/publish")
async def blog_toggle_publish(
    request: Request,
    post_id: int,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """Toggle publish status of a blog post."""
    async for db in get_db():
        post = await blog_service_db.get_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        await blog_service_db.toggle_publish(db, post)

    return RedirectResponse(url="/admin/blog", status_code=302)
