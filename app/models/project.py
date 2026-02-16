from datetime import datetime

from pydantic import BaseModel


class Project(BaseModel):
    id: int
    title: str
    description: str
    technologies: list[str]
    github_url: str | None = None
    demo_url: str | None = None
    image_url: str | None = None
    created_at: datetime | None = None
    featured: bool = False


class ProjectCreate(BaseModel):
    title: str
    description: str
    technologies: list[str]
    github_url: str | None = None
    demo_url: str | None = None
    image_url: str | None = None
    featured: bool = False
