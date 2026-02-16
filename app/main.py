import html
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

from app.database.connection import close_db, init_db
from app.middleware import limiter
from app.routers import admin, api, auth, blog, demos, pages, projects
from app.services.blog import blog_service
from app.services.project import project_service

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="Brian Hardin - Personal Brand",
    description="Personal website showcasing Python projects and skills",
    version="1.0.0",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(pages.router)
app.include_router(projects.router, prefix="/projects")
app.include_router(api.router, prefix="/api")
app.include_router(blog.router)
app.include_router(demos.router, prefix="/demos")
app.include_router(auth.router)
app.include_router(admin.router)


@app.exception_handler(401)
async def unauthorized_handler(
    request: Request, exc: StarletteHTTPException
) -> Response:
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        return RedirectResponse(url="/admin/login", status_code=302)
    return Response(content="Unauthorized", status_code=401, media_type="text/plain")


@app.exception_handler(403)
async def forbidden_handler(request: Request, exc: StarletteHTTPException) -> Response:
    detail = getattr(exc, "detail", "")
    if "CSRF" in str(detail):
        html_content = """<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
<strong>Session expired.</strong> Please reload the page and try again.
</div>"""
        return HTMLResponse(content=html_content, status_code=403)
    return Response(content="Forbidden", status_code=403, media_type="text/plain")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: StarletteHTTPException) -> Response:
    return templates.TemplateResponse(
        request,
        "errors/404.html",
        context={"current_page": ""},
        status_code=404,
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc: Exception) -> Response:
    try:
        return templates.TemplateResponse(
            request,
            "errors/500.html",
            context={"current_page": ""},
            status_code=500,
        )
    except Exception:
        logger.exception("Failed to render 500 error page")
        return Response(
            content="Internal Server Error", status_code=500, media_type="text/plain"
        )


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request) -> Response:
    featured_projects = project_service.get_featured(limit=2)
    featured_posts = blog_service.get_posts_summary(published_only=True, limit=2)
    return templates.TemplateResponse(
        request,
        "index.html",
        context={
            "current_page": "home",
            "projects": featured_projects,
            "featured_posts": featured_posts,
        },
    )


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/sitemap.xml")
async def sitemap() -> Response:
    """XML sitemap for search engines."""
    today = datetime.now().strftime("%Y-%m-%d")

    urls: list[tuple[str, str, str]] = [
        # (path, changefreq, priority)
        ("/", "weekly", "1.0"),
        ("/about", "monthly", "0.8"),
        ("/contact", "monthly", "0.7"),
        ("/resume", "monthly", "0.8"),
        ("/blog", "weekly", "0.9"),
        ("/projects", "weekly", "0.9"),
        ("/demos", "monthly", "0.8"),
    ]

    # Project detail pages
    for pid in [3, 4, 6, 7, 8]:
        urls.append((f"/projects/{pid}", "monthly", "0.7"))

    # Published blog post slugs
    posts = blog_service.get_all_posts(published_only=True)
    for post in posts:
        urls.append((f"/blog/{post.slug}", "monthly", "0.7"))

    # Demo pages
    demo_pages = [
        "payment-processing",
        "data-pipeline",
        "sales-dashboard",
        "collections-dashboard",
        "automation-suite",
    ]
    for page in demo_pages:
        urls.append((f"/demos/{page}", "monthly", "0.6"))

    xml_entries = []
    for path, changefreq, priority in urls:
        escaped_path = html.escape(path)
        xml_entries.append(
            f"""  <url>
    <loc>https://brianhardin.info{escaped_path}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(xml_entries)}
</urlset>"""

    return Response(content=xml_content, media_type="application/xml")


@app.get("/service-worker.js")
async def service_worker() -> Response:
    """Minimal service worker to prevent 404 errors"""
    content = """
// Minimal service worker
self.addEventListener('install', function(event) {
    self.skipWaiting();
});

self.addEventListener('activate', function(event) {
    event.waitUntil(self.clients.claim());
});
    """.strip()

    return Response(content=content, media_type="application/javascript")
