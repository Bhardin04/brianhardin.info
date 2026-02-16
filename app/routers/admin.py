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
from app.services.contact_db import contact_message_service
from app.services.project_db import project_service_db
from app.services.settings_db import site_settings_service

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


def _parse_lines(text: str) -> list[str]:
    """Parse newline-separated text into a list of strings."""
    if not text.strip():
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


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


# ---------- Project CRUD ----------


@router.get("/projects", response_class=HTMLResponse)
async def project_list(
    request: Request,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """List all projects."""
    projects: list[Project] = []
    async for db in get_db():
        projects = await project_service_db.get_all(db)

    for proj in projects:
        proj.tech_list = _tags_list_from_json(proj.technologies)  # type: ignore[attr-defined]

    return templates.TemplateResponse(
        request,
        "admin/projects/list.html",
        context={
            "admin_user": session.github_username,
            "projects": projects,
        },
    )


@router.get("/projects/new", response_class=HTMLResponse)
async def project_new_form(
    request: Request,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """New project form."""
    csrf = generate_csrf_token()
    response = templates.TemplateResponse(
        request,
        "admin/projects/edit.html",
        context={
            "admin_user": session.github_username,
            "project": None,
            "csrf_token": csrf,
        },
    )
    response.set_cookie("csrf_token", csrf, httponly=True, samesite="strict")
    return response


@router.post("/projects/new")
async def project_create(
    request: Request,
    session: AdminSession = Depends(require_admin),
    title: str = Form(...),
    description: str = Form(""),
    long_description: str = Form(""),
    technologies: str = Form(""),
    category: str = Form("web_app"),
    status: str = Form("completed"),
    featured: str = Form(""),
    sort_order: int = Form(0),
    image_url: str = Form(""),
    github_url: str = Form(""),
    demo_url: str = Form(""),
    duration: str = Form(""),
    role: str = Form(""),
    team_size: str = Form(""),
    client_type: str = Form(""),
    features: str = Form(""),
    challenges: str = Form(""),
    csrf_token: str = Form(...),
) -> Response:
    """Create a new project."""
    cookie_csrf = request.cookies.get("csrf_token", "")
    if csrf_token != cookie_csrf or not validate_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    async for db in get_db():
        await project_service_db.create(
            db,
            title=title,
            description=description,
            long_description=long_description,
            technologies=_parse_tags(technologies),
            category=category,
            status=status,
            featured=featured == "true",
            sort_order=sort_order,
            image_url=image_url,
            github_url=github_url,
            demo_url=demo_url,
            duration=duration,
            role=role,
            team_size=team_size,
            client_type=client_type,
            features=_parse_lines(features),
            challenges=_parse_lines(challenges),
        )

    return RedirectResponse(url="/admin/projects", status_code=302)


@router.get("/projects/{project_id}/edit", response_class=HTMLResponse)
async def project_edit_form(
    request: Request,
    project_id: int,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """Edit project form."""
    async for db in get_db():
        project = await project_service_db.get_by_id(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        project.tech_list = _tags_list_from_json(project.technologies)  # type: ignore[attr-defined]
        project.features_list = _tags_list_from_json(project.features)  # type: ignore[attr-defined]
        project.challenges_list = _tags_list_from_json(project.challenges)  # type: ignore[attr-defined]

        csrf = generate_csrf_token()
        response = templates.TemplateResponse(
            request,
            "admin/projects/edit.html",
            context={
                "admin_user": session.github_username,
                "project": project,
                "csrf_token": csrf,
            },
        )
        response.set_cookie("csrf_token", csrf, httponly=True, samesite="strict")
        return response

    raise HTTPException(status_code=500, detail="Database unavailable")


@router.post("/projects/{project_id}/edit")
async def project_update(
    request: Request,
    project_id: int,
    session: AdminSession = Depends(require_admin),
    title: str = Form(...),
    description: str = Form(""),
    long_description: str = Form(""),
    technologies: str = Form(""),
    category: str = Form("web_app"),
    status: str = Form("completed"),
    featured: str = Form(""),
    sort_order: int = Form(0),
    image_url: str = Form(""),
    github_url: str = Form(""),
    demo_url: str = Form(""),
    duration: str = Form(""),
    role: str = Form(""),
    team_size: str = Form(""),
    client_type: str = Form(""),
    features: str = Form(""),
    challenges: str = Form(""),
    csrf_token: str = Form(...),
) -> Response:
    """Update an existing project."""
    cookie_csrf = request.cookies.get("csrf_token", "")
    if csrf_token != cookie_csrf or not validate_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    async for db in get_db():
        project = await project_service_db.get_by_id(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        await project_service_db.update(
            db,
            project,
            title=title,
            description=description,
            long_description=long_description,
            technologies=_parse_tags(technologies),
            category=category,
            status=status,
            featured=featured == "true",
            sort_order=sort_order,
            image_url=image_url,
            github_url=github_url,
            demo_url=demo_url,
            duration=duration,
            role=role,
            team_size=team_size,
            client_type=client_type,
            features=_parse_lines(features),
            challenges=_parse_lines(challenges),
        )

    return RedirectResponse(url="/admin/projects", status_code=302)


@router.post("/projects/{project_id}/delete")
async def project_delete(
    request: Request,
    project_id: int,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """Delete a project."""
    async for db in get_db():
        project = await project_service_db.get_by_id(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        await project_service_db.delete(db, project)

    return RedirectResponse(url="/admin/projects", status_code=302)


# ---------- Messages ----------


@router.get("/messages", response_class=HTMLResponse)
async def messages_list(
    request: Request,
    session: AdminSession = Depends(require_admin),
    archived: str = "",
) -> Response:
    """List contact messages."""
    show_archived = archived.lower() == "true"
    messages: list[ContactMessage] = []
    async for db in get_db():
        messages = await contact_message_service.get_all(db, archived=show_archived)

    return templates.TemplateResponse(
        request,
        "admin/messages/list.html",
        context={
            "admin_user": session.github_username,
            "messages": messages,
            "show_archived": show_archived,
        },
    )


@router.get("/messages/{message_id}", response_class=HTMLResponse)
async def message_detail(
    request: Request,
    message_id: int,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """View a single message (marks as read)."""
    async for db in get_db():
        msg = await contact_message_service.get_by_id(db, message_id)
        if not msg:
            raise HTTPException(status_code=404, detail="Message not found")

        if not msg.read:
            await contact_message_service.mark_read(db, msg)

        return templates.TemplateResponse(
            request,
            "admin/messages/detail.html",
            context={
                "admin_user": session.github_username,
                "msg": msg,
            },
        )

    raise HTTPException(status_code=500, detail="Database unavailable")


@router.post("/messages/{message_id}/archive")
async def message_archive(
    request: Request,
    message_id: int,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """Toggle archive status of a message."""
    async for db in get_db():
        msg = await contact_message_service.get_by_id(db, message_id)
        if not msg:
            raise HTTPException(status_code=404, detail="Message not found")
        await contact_message_service.toggle_archive(db, msg)

    return RedirectResponse(url="/admin/messages", status_code=302)


@router.post("/messages/{message_id}/delete")
async def message_delete(
    request: Request,
    message_id: int,
    session: AdminSession = Depends(require_admin),
) -> Response:
    """Delete a message."""
    async for db in get_db():
        msg = await contact_message_service.get_by_id(db, message_id)
        if not msg:
            raise HTTPException(status_code=404, detail="Message not found")
        await contact_message_service.delete(db, msg)

    return RedirectResponse(url="/admin/messages", status_code=302)


# ---------- Settings ----------


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    session: AdminSession = Depends(require_admin),
    saved: str = "",
) -> Response:
    """Site settings page."""
    settings: dict[str, str] = {}
    async for db in get_db():
        settings = await site_settings_service.get_all(db)

    csrf = generate_csrf_token()
    response = templates.TemplateResponse(
        request,
        "admin/settings.html",
        context={
            "admin_user": session.github_username,
            "settings": settings,
            "csrf_token": csrf,
            "saved": saved == "true",
        },
    )
    response.set_cookie("csrf_token", csrf, httponly=True, samesite="strict")
    return response


@router.post("/settings")
async def settings_save(
    request: Request,
    session: AdminSession = Depends(require_admin),
    site_title: str = Form(""),
    site_description: str = Form(""),
    contact_email: str = Form(""),
    github_url: str = Form(""),
    linkedin_url: str = Form(""),
    twitter_url: str = Form(""),
    csrf_token: str = Form(...),
) -> Response:
    """Save site settings."""
    cookie_csrf = request.cookies.get("csrf_token", "")
    if csrf_token != cookie_csrf or not validate_csrf_token(csrf_token):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")

    async for db in get_db():
        await site_settings_service.set_many(
            db,
            {
                "site_title": site_title,
                "site_description": site_description,
                "contact_email": contact_email,
                "github_url": github_url,
                "linkedin_url": linkedin_url,
                "twitter_url": twitter_url,
            },
        )

    return RedirectResponse(url="/admin/settings?saved=true", status_code=302)
