from datetime import datetime

from pydantic import BaseModel, Field


class BlogPost(BaseModel):
    """Blog post model with markdown content support."""

    id: int
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    excerpt: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    content_html: str | None = None
    tags: list[str] = Field(default_factory=list)
    published: bool = Field(default=False)
    featured: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    published_at: datetime | None = None
    reading_time_minutes: int | None = None
    author: str = Field(default="Brian Hardin")
    meta_description: str | None = None
    og_image: str | None = None


class BlogPostCreate(BaseModel):
    """Model for creating new blog posts."""

    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    excerpt: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    tags: list[str] = Field(default_factory=list)
    published: bool = Field(default=False)
    featured: bool = Field(default=False)
    meta_description: str | None = None
    og_image: str | None = None


class BlogPostUpdate(BaseModel):
    """Model for updating existing blog posts."""

    title: str | None = Field(None, min_length=1, max_length=200)
    slug: str | None = Field(None, min_length=1, max_length=200)
    excerpt: str | None = Field(None, min_length=1, max_length=500)
    content: str | None = None
    tags: list[str] | None = None
    published: bool | None = None
    featured: bool | None = None
    meta_description: str | None = None
    og_image: str | None = None


class BlogPostSummary(BaseModel):
    """Lightweight blog post model for listings."""

    id: int
    title: str
    slug: str
    excerpt: str
    tags: list[str]
    published: bool
    featured: bool
    created_at: datetime
    published_at: datetime | None
    reading_time_minutes: int | None
    author: str
