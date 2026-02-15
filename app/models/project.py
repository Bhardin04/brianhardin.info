from datetime import datetime

from pydantic import BaseModel, HttpUrl


class Project(BaseModel):
    id: int
    title: str
    description: str
    technologies: list[str]
    github_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None
    image_url: str | None = None
    created_at: datetime | None = None
    featured: bool = False


class ProjectCreate(BaseModel):
    title: str
    description: str
    technologies: list[str]
    github_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None
    image_url: str | None = None
    featured: bool = False
