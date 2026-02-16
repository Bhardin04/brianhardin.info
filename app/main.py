from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from app.models.project import Project
from app.routers import api, blog, pages, projects
from app.services.blog import blog_service

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


@app.get("/service-worker.js")
async def service_worker():
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

    from fastapi.responses import Response

    return Response(content=content, media_type="application/javascript")
