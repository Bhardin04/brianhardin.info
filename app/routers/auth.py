"""GitHub OAuth authentication routes for admin panel."""

import logging
import secrets
from datetime import UTC, datetime, timedelta

import httpx
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select

from app.config import settings
from app.database.connection import get_db
from app.database.models import AdminSession

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

SESSION_TTL_HOURS = 24
GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request) -> Response:
    """Render the admin login page."""
    return templates.TemplateResponse(request, "admin/login.html")


@router.get("/login/github")
async def login_github(request: Request) -> Response:
    """Redirect to GitHub OAuth authorization page."""
    if not settings.GITHUB_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GitHub OAuth not configured")

    state = secrets.token_urlsafe(32)
    redirect_uri = str(request.url_for("github_callback"))

    response = RedirectResponse(
        url=(
            f"{GITHUB_AUTHORIZE_URL}"
            f"?client_id={settings.GITHUB_CLIENT_ID}"
            f"&redirect_uri={redirect_uri}"
            f"&scope=read:user"
            f"&state={state}"
        ),
        status_code=302,
    )
    response.set_cookie(
        "oauth_state",
        state,
        max_age=600,
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/callback", name="github_callback")
async def github_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
) -> Response:
    """Handle GitHub OAuth callback."""
    # Validate state to prevent CSRF
    stored_state = request.cookies.get("oauth_state")
    if not state or not stored_state or state != stored_state:
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )

        if token_response.status_code != 200:
            logger.error("GitHub token exchange failed: %s", token_response.text)
            raise HTTPException(status_code=400, detail="OAuth token exchange failed")

        token_data = token_response.json()
        access_token = token_data.get("access_token")
        if not access_token:
            raise HTTPException(status_code=400, detail="No access token received")

        # Fetch GitHub user info
        user_response = await client.get(
            GITHUB_USER_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch GitHub user")

        user_data = user_response.json()

    github_username = user_data.get("login", "")
    github_id = user_data.get("id", 0)

    # Verify this is the authorized admin user
    if github_username.lower() != settings.ADMIN_GITHUB_USERNAME.lower():
        logger.warning("Unauthorized login attempt by GitHub user: %s", github_username)
        raise HTTPException(status_code=403, detail="Not authorized")

    # Create admin session
    session_token = secrets.token_urlsafe(48)
    expires_at = datetime.now(UTC) + timedelta(hours=SESSION_TTL_HOURS)

    async for db in get_db():
        admin_session = AdminSession(
            session_token=session_token,
            github_username=github_username,
            github_id=github_id,
            expires_at=expires_at,
        )
        db.add(admin_session)
        await db.commit()

    response = RedirectResponse(url="/admin/", status_code=302)
    response.set_cookie(
        "admin_session",
        session_token,
        max_age=SESSION_TTL_HOURS * 3600,
        httponly=True,
        samesite="lax",
    )
    # Clean up the OAuth state cookie
    response.delete_cookie("oauth_state")
    return response


@router.post("/logout")
async def logout(request: Request) -> Response:
    """Log out by deleting the session."""
    session_token = request.cookies.get("admin_session")
    if session_token:
        async for db in get_db():
            result = await db.execute(
                select(AdminSession).where(AdminSession.session_token == session_token)
            )
            session = result.scalar_one_or_none()
            if session:
                await db.delete(session)
                await db.commit()

    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("admin_session")
    return response
