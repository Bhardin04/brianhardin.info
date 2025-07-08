from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class BlogPost(BaseModel):
    """Blog post model with markdown content support."""
    
    id: int
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    excerpt: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    content_html: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    published: bool = Field(default=False)
    featured: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    reading_time_minutes: Optional[int] = None
    author: str = Field(default="Brian Hardin")
    meta_description: Optional[str] = None
    og_image: Optional[str] = None


class BlogPostCreate(BaseModel):
    """Model for creating new blog posts."""
    
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    excerpt: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    tags: List[str] = Field(default_factory=list)
    published: bool = Field(default=False)
    featured: bool = Field(default=False)
    meta_description: Optional[str] = None
    og_image: Optional[str] = None


class BlogPostUpdate(BaseModel):
    """Model for updating existing blog posts."""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    slug: Optional[str] = Field(None, min_length=1, max_length=200)
    excerpt: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    tags: Optional[List[str]] = None
    published: Optional[bool] = None
    featured: Optional[bool] = None
    meta_description: Optional[str] = None
    og_image: Optional[str] = None


class BlogPostSummary(BaseModel):
    """Lightweight blog post model for listings."""
    
    id: int
    title: str
    slug: str
    excerpt: str
    tags: List[str]
    published: bool
    featured: bool
    created_at: datetime
    published_at: Optional[datetime]
    reading_time_minutes: Optional[int]
    author: str