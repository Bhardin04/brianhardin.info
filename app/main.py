from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.routers import pages, projects, api, blog

app = FastAPI(
    title="Brian Hardin - Personal Brand",
    description="Personal website showcasing Python projects and skills",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(pages.router)
app.include_router(projects.router, prefix="/projects")
app.include_router(api.router, prefix="/api")
app.include_router(blog.router)

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}