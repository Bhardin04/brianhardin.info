from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from app.config import settings
from app.middleware import CSRF_COOKIE_NAME, generate_csrf_token

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/about", response_class=HTMLResponse)
async def about(request: Request) -> Response:
    return templates.TemplateResponse(
        "about.html", {"request": request, "current_page": "about"}
    )


@router.get("/contact", response_class=HTMLResponse)
async def contact(request: Request) -> Response:
    csrf_token = generate_csrf_token()
    response = templates.TemplateResponse(
        "contact.html",
        {"request": request, "current_page": "contact", "csrf_token": csrf_token},
    )
    response.set_cookie(
        key=CSRF_COOKIE_NAME,
        value=csrf_token,
        httponly=True,
        samesite="strict",
        secure=not settings.DEBUG,
    )
    return response


@router.get("/resume", response_class=HTMLResponse)
async def resume(request: Request) -> Response:
    return templates.TemplateResponse(
        "resume.html", {"request": request, "current_page": "resume"}
    )
