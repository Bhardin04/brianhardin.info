import html
import logging
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import Response

from app.models.project import Project
from app.routers import api, blog, demos, pages, projects
from app.services.blog import blog_service

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Brian Hardin - Personal Brand",
    description="Personal website showcasing Python projects and skills",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(pages.router)
app.include_router(projects.router, prefix="/projects")
app.include_router(api.router, prefix="/api")
app.include_router(blog.router)
app.include_router(demos.router, prefix="/demos")


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: StarletteHTTPException) -> Response:
    return templates.TemplateResponse(
        "errors/404.html",
        {"request": request, "current_page": ""},
        status_code=404,
    )


@app.exception_handler(500)
async def server_error_handler(
    request: Request, exc: StarletteHTTPException
) -> Response:
    try:
        return templates.TemplateResponse(
            "errors/500.html",
            {"request": request, "current_page": ""},
            status_code=500,
        )
    except Exception:
        logger.exception("Failed to render 500 error page")
        return Response(
            content="Internal Server Error", status_code=500, media_type="text/plain"
        )


@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request) -> Response:
    featured_projects = [
        Project(
            id=1,
            title="Personal Website",
            description="FastAPI-based personal brand website with HTMX interactions, dark mode, and responsive design",
            technologies=["Python", "FastAPI", "Jinja2", "HTMX"],
            github_url="https://github.com/Bhardin04/brianhardin.info",
            demo_url="https://brianhardin.info",
        ),
        Project(
            id=2,
            title="REST API Toolkit",
            description="Production-ready FastAPI starter with authentication, database integration, and auto-generated docs",
            technologies=["Python", "FastAPI", "PostgreSQL", "Docker"],
            github_url="https://github.com/Bhardin04",
        ),
    ]
    featured_posts = blog_service.get_posts_summary(published_only=True, limit=2)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
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
