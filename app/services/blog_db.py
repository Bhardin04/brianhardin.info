"""Database-backed blog service with CRUD operations."""

import json
import logging
import re

import markdown  # type: ignore[import-untyped]
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import BlogPost

logger = logging.getLogger(__name__)

# Shared markdown processor
_md = markdown.Markdown(
    extensions=["codehilite", "toc", "tables", "fenced_code", "attr_list"],
    extension_configs={
        "codehilite": {"css_class": "highlight", "use_pygments": True},
        "toc": {"permalink": True},
    },
)


def calculate_reading_time(content: str) -> int:
    """Calculate estimated reading time in minutes."""
    text = re.sub(r"[#*`_\[\](){}]", "", content)
    words = len(text.split())
    return max(1, round(words / 200))


def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title."""
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug.strip("-")


def render_markdown(content: str) -> str:
    """Convert markdown content to HTML."""
    _md.reset()
    result: str = _md.convert(content)
    return result


class BlogServiceDB:
    """Database-backed blog service."""

    async def get_all(
        self, db: AsyncSession, *, published_only: bool = False
    ) -> list[BlogPost]:
        stmt = select(BlogPost).order_by(BlogPost.created_at.desc())
        if published_only:
            stmt = stmt.where(BlogPost.published == True)  # noqa: E712
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, post_id: int) -> BlogPost | None:
        result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
        row: BlogPost | None = result.scalar_one_or_none()
        return row

    async def get_by_slug(self, db: AsyncSession, slug: str) -> BlogPost | None:
        result = await db.execute(select(BlogPost).where(BlogPost.slug == slug))
        row: BlogPost | None = result.scalar_one_or_none()
        return row

    async def create(
        self,
        db: AsyncSession,
        *,
        title: str,
        slug: str,
        content: str,
        excerpt: str = "",
        tags: list[str] | None = None,
        published: bool = False,
        featured: bool = False,
        author: str = "Brian Hardin",
        meta_description: str = "",
    ) -> BlogPost:
        content_html = render_markdown(content)
        reading_time = calculate_reading_time(content)

        post = BlogPost(
            title=title,
            slug=slug or generate_slug(title),
            content=content,
            content_html=content_html,
            excerpt=excerpt,
            tags=json.dumps(tags or []),
            published=published,
            featured=featured,
            author=author,
            meta_description=meta_description,
            reading_time_minutes=reading_time,
        )
        db.add(post)
        await db.flush()
        await db.commit()
        return post

    async def update(
        self,
        db: AsyncSession,
        post: BlogPost,
        *,
        title: str,
        slug: str,
        content: str,
        excerpt: str = "",
        tags: list[str] | None = None,
        published: bool = False,
        featured: bool = False,
        author: str = "Brian Hardin",
        meta_description: str = "",
    ) -> BlogPost:
        post.title = title
        post.slug = slug or generate_slug(title)
        post.content = content
        post.content_html = render_markdown(content)
        post.excerpt = excerpt
        post.tags = json.dumps(tags or [])
        post.published = published
        post.featured = featured
        post.author = author
        post.meta_description = meta_description
        post.reading_time_minutes = calculate_reading_time(content)

        await db.commit()
        return post

    async def delete(self, db: AsyncSession, post: BlogPost) -> None:
        await db.delete(post)
        await db.commit()

    async def toggle_publish(self, db: AsyncSession, post: BlogPost) -> BlogPost:
        post.published = not post.published
        await db.commit()
        return post

    async def count(self, db: AsyncSession) -> int:
        result = await db.execute(select(BlogPost.id))
        return len(result.all())


blog_service_db = BlogServiceDB()
