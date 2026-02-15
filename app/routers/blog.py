from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import Response

from app.models.blog import BlogPost, BlogPostSummary
from app.services.blog import blog_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/blog", response_class=HTMLResponse)
async def blog_list(request: Request, tag: str | None = None) -> Response:
    """Blog listing page with optional tag filtering."""
    posts: list[BlogPost] | list[BlogPostSummary]
    if tag:
        posts = blog_service.get_posts_by_tag(tag)
        page_title = f"Blog Posts Tagged '{tag}'"
    else:
        posts = blog_service.get_posts_summary(published_only=True)
        page_title = "Technical Blog"

    # Get all unique tags for the sidebar
    all_posts = blog_service.get_all_posts()
    all_tags = set()
    for post in all_posts:
        all_tags.update(post.tags)

    featured_posts = blog_service.get_featured_posts(limit=3)

    return templates.TemplateResponse(
        "blog/index.html",
        {
            "request": request,
            "posts": posts,
            "featured_posts": featured_posts,
            "all_tags": sorted(all_tags),
            "current_tag": tag,
            "page_title": page_title,
        },
    )


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_post(request: Request, slug: str) -> Response:
    """Individual blog post page."""
    post = blog_service.get_post_by_slug(slug)

    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")

    if not post.published:
        raise HTTPException(status_code=404, detail="Blog post not found")

    # Get related posts (same tags)
    related_posts = []
    if post.tags:
        all_posts = blog_service.get_all_posts()
        for other_post in all_posts:
            if other_post.id != post.id and any(
                tag in other_post.tags for tag in post.tags
            ):
                related_posts.append(other_post)
                if len(related_posts) >= 3:
                    break

    return templates.TemplateResponse(
        "blog/post.html",
        {"request": request, "post": post, "related_posts": related_posts},
    )


# API endpoints for blog data
@router.get("/api/blog/posts")
async def api_get_posts(
    published_only: bool = True, limit: int | None = None, tag: str | None = None
) -> list[BlogPost] | list[BlogPostSummary]:
    """API endpoint to get blog posts."""
    api_posts: list[BlogPost] | list[BlogPostSummary]
    if tag:
        api_posts = blog_service.get_posts_by_tag(tag)
        if published_only:
            api_posts = [post for post in api_posts if post.published]
    else:
        api_posts = blog_service.get_posts_summary(
            published_only=published_only, limit=limit
        )

    return api_posts


@router.get("/api/blog/posts/{slug}")
async def api_get_post(slug: str) -> BlogPost:
    """API endpoint to get a specific blog post."""
    post = blog_service.get_post_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return post


@router.get("/api/blog/featured")
async def api_get_featured_posts(limit: int = 3) -> list[BlogPost]:
    """API endpoint to get featured blog posts."""
    return blog_service.get_featured_posts(limit=limit)


@router.get("/api/blog/tags")
async def api_get_tags() -> list[str]:
    """API endpoint to get all blog tags."""
    posts = blog_service.get_all_posts()
    tags: set[str] = set()
    for post in posts:
        tags.update(post.tags)
    return sorted(tags)
