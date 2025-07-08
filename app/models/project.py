from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class Project(BaseModel):
    id: int
    title: str
    description: str
    technologies: List[str]
    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    featured: bool = False

class ProjectCreate(BaseModel):
    title: str
    description: str
    technologies: List[str]
    github_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    image_url: Optional[str] = None
    featured: bool = False