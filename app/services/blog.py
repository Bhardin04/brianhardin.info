import re
from datetime import datetime
from pathlib import Path

import frontmatter
import markdown

from app.models.blog import BlogPost, BlogPostSummary


class BlogService:
    """Service for managing blog posts with markdown content."""

    def __init__(self, posts_directory: str = "content/blog"):
        self.posts_directory = Path(posts_directory)
        self.posts_directory.mkdir(parents=True, exist_ok=True)

        # Configure markdown with extensions
        self.md = markdown.Markdown(
            extensions=["codehilite", "toc", "tables", "fenced_code", "attr_list"],
            extension_configs={
                "codehilite": {"css_class": "highlight", "use_pygments": True},
                "toc": {"permalink": True},
            },
        )

    def _calculate_reading_time(self, content: str) -> int:
        """Calculate estimated reading time in minutes."""
        # Remove markdown syntax and count words
        text = re.sub(r"[#*`_\[\](){}]", "", content)
        words = len(text.split())
        # Average reading speed: 200 words per minute
        return max(1, round(words / 200))

    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title."""
        slug = re.sub(r"[^\w\s-]", "", title.lower())
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug.strip("-")

    def _load_post_from_file(self, file_path: Path) -> BlogPost | None:
        """Load a blog post from a markdown file with frontmatter."""
        try:
            with open(file_path, encoding="utf-8") as f:
                post = frontmatter.load(f)

            # Extract frontmatter metadata
            metadata = post.metadata
            content = post.content

            # Convert markdown to HTML
            content_html = self.md.convert(content)

            # Generate values if not provided
            slug = metadata.get("slug") or self._generate_slug(metadata["title"])
            reading_time = self._calculate_reading_time(content)

            # Parse dates
            created_at = metadata.get("created_at")
            if isinstance(created_at, str):
                created_at = datetime.fromisoformat(created_at)
            elif not created_at:
                created_at = datetime.fromtimestamp(file_path.stat().st_mtime)

            published_at = metadata.get("published_at")
            if isinstance(published_at, str):
                published_at = datetime.fromisoformat(published_at)
            elif metadata.get("published", False) and not published_at:
                published_at = created_at

            return BlogPost(
                id=metadata.get("id", hash(slug) % 10000),
                title=metadata["title"],
                slug=slug,
                excerpt=metadata.get("excerpt", ""),
                content=content,
                content_html=content_html,
                tags=metadata.get("tags", []),
                published=metadata.get("published", False),
                featured=metadata.get("featured", False),
                created_at=created_at,
                published_at=published_at,
                reading_time_minutes=reading_time,
                author=metadata.get("author", "Brian Hardin"),
                meta_description=metadata.get("meta_description"),
                og_image=metadata.get("og_image"),
            )
        except Exception as e:
            print(f"Error loading post from {file_path}: {e}")
            return None

    def get_all_posts(self, published_only: bool = True) -> list[BlogPost]:
        """Get all blog posts, optionally filtered by published status."""
        # For now, return sample posts since we don't have markdown files yet
        sample_posts = self._get_sample_posts()

        if published_only:
            return [post for post in sample_posts if post.published]
        return sample_posts

    def get_posts_summary(
        self, published_only: bool = True, limit: int | None = None
    ) -> list[BlogPostSummary]:
        """Get blog post summaries for listing pages."""
        posts = self.get_all_posts(published_only)

        # Sort by published date (newest first)
        posts.sort(key=lambda p: p.published_at or p.created_at, reverse=True)

        if limit:
            posts = posts[:limit]

        return [
            BlogPostSummary(
                id=post.id,
                title=post.title,
                slug=post.slug,
                excerpt=post.excerpt,
                tags=post.tags,
                published=post.published,
                featured=post.featured,
                created_at=post.created_at,
                published_at=post.published_at,
                reading_time_minutes=post.reading_time_minutes,
                author=post.author,
            )
            for post in posts
        ]

    def get_post_by_slug(self, slug: str) -> BlogPost | None:
        """Get a specific blog post by its slug."""
        posts = self.get_all_posts(published_only=False)
        for post in posts:
            if post.slug == slug:
                return post
        return None

    def get_post_by_id(self, post_id: int) -> BlogPost | None:
        """Get a specific blog post by its ID."""
        posts = self.get_all_posts(published_only=False)
        for post in posts:
            if post.id == post_id:
                return post
        return None

    def get_featured_posts(self, limit: int = 3) -> list[BlogPost]:
        """Get featured blog posts."""
        posts = [post for post in self.get_all_posts() if post.featured]
        posts.sort(key=lambda p: p.published_at or p.created_at, reverse=True)
        return posts[:limit]

    def get_posts_by_tag(self, tag: str) -> list[BlogPost]:
        """Get blog posts filtered by tag."""
        posts = self.get_all_posts()
        return [post for post in posts if tag.lower() in [t.lower() for t in post.tags]]

    def _get_sample_posts(self) -> list[BlogPost]:
        """Generate sample blog posts for demonstration."""
        return [
            BlogPost(
                id=1,
                title="Building Modern Web Applications with FastAPI and HTMX",
                slug="fastapi-htmx-modern-web-apps",
                excerpt="Discover how to create interactive, modern web applications using FastAPI for the backend and HTMX for dynamic frontend interactions without complex JavaScript frameworks.",
                content="""# Building Modern Web Applications with FastAPI and HTMX

In this comprehensive guide, we'll explore how to build modern, interactive web applications using FastAPI and HTMX.

## Why FastAPI + HTMX?

The combination of FastAPI and HTMX offers several advantages:

- **Simplicity**: No complex JavaScript build tools or frameworks
- **Performance**: Fast server-side rendering with dynamic updates
- **Developer Experience**: Python-first development with minimal frontend complexity
- **SEO-Friendly**: Server-rendered content that search engines love

## Getting Started

First, let's set up our FastAPI application:

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
```

## Adding HTMX Interactions

HTMX allows you to add AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML:

```html
<button hx-post="/api/contact"
        hx-target="#form-message"
        hx-swap="innerHTML">
    Send Message
</button>
```

This creates a seamless user experience without page reloads.""",
                content_html="<p>HTML content would be generated here...</p>",
                tags=["Python", "FastAPI", "HTMX", "Web Development"],
                published=True,
                featured=True,
                created_at=datetime(2024, 12, 1),
                published_at=datetime(2024, 12, 1),
                reading_time_minutes=8,
                author="Brian Hardin",
                meta_description="Learn how to build modern web applications using FastAPI and HTMX for interactive, fast, and SEO-friendly websites.",
                og_image="/static/images/blog/fastapi-htmx-cover.jpg",
            ),
            BlogPost(
                id=2,
                title="Mastering Async Python: From Basics to Production",
                slug="mastering-async-python-production",
                excerpt="A deep dive into asynchronous Python programming, covering asyncio fundamentals, best practices, and real-world production patterns for scalable applications.",
                content="""# Mastering Async Python: From Basics to Production

Asynchronous programming in Python has become essential for building scalable, high-performance applications.

## Understanding Asyncio

The `asyncio` library provides the foundation for asynchronous programming in Python:

```python
import asyncio

async def fetch_data(url):
    # Simulate async operation
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    tasks = [
        fetch_data("https://api1.example.com"),
        fetch_data("https://api2.example.com"),
        fetch_data("https://api3.example.com")
    ]
    results = await asyncio.gather(*tasks)
    return results
```

## Production Patterns

When building production applications, consider these patterns:

1. **Connection Pooling**: Reuse database connections
2. **Rate Limiting**: Prevent overwhelming external APIs
3. **Error Handling**: Graceful degradation and retries
4. **Monitoring**: Track async operation performance""",
                content_html="<p>HTML content would be generated here...</p>",
                tags=["Python", "Asyncio", "Performance", "Backend"],
                published=True,
                featured=False,
                created_at=datetime(2024, 11, 15),
                published_at=datetime(2024, 11, 15),
                reading_time_minutes=12,
                author="Brian Hardin",
                meta_description="Master asynchronous Python programming with practical examples and production-ready patterns for scalable applications.",
                og_image="/static/images/blog/async-python-cover.jpg",
            ),
            BlogPost(
                id=3,
                title="Docker Best Practices for Python Applications",
                slug="docker-best-practices-python",
                excerpt="Learn essential Docker best practices for Python applications, including multi-stage builds, security considerations, and optimization techniques for production deployments.",
                content="""# Docker Best Practices for Python Applications

Docker has revolutionized how we deploy Python applications. Here are the essential best practices.

## Multi-Stage Builds

Use multi-stage builds to reduce image size:

```dockerfile
# Build stage
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
CMD ["python", "app.py"]
```

## Security Considerations

1. **Use official base images**
2. **Run as non-root user**
3. **Scan for vulnerabilities**
4. **Keep dependencies updated**""",
                content_html="<p>HTML content would be generated here...</p>",
                tags=["Docker", "Python", "DevOps", "Security"],
                published=True,
                featured=False,
                created_at=datetime(2024, 11, 1),
                published_at=datetime(2024, 11, 1),
                reading_time_minutes=6,
                author="Brian Hardin",
                meta_description="Essential Docker best practices for Python applications including security, optimization, and production deployment strategies.",
                og_image="/static/images/blog/docker-python-cover.jpg",
            ),
            BlogPost(
                id=4,
                title="Testing FastAPI Applications: A Comprehensive Guide",
                slug="testing-fastapi-comprehensive-guide",
                excerpt="Complete guide to testing FastAPI applications, covering unit tests, integration tests, database testing, and automated testing strategies for robust applications.",
                content="""# Testing FastAPI Applications: A Comprehensive Guide

Testing is crucial for building reliable FastAPI applications. This guide covers everything you need to know.

## Setting Up Testing

First, let's set up our testing environment:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Brian Hardin" in response.text
```

## Database Testing

For database testing, use fixtures and test databases:

```python
@pytest.fixture
def test_db():
    # Create test database
    engine = create_engine("sqlite:///test.db")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield TestingSessionLocal()

    # Cleanup
    Base.metadata.drop_all(bind=engine)
```

## API Testing Strategies

Test your API endpoints thoroughly:

1. **Happy paths**: Normal successful requests
2. **Error cases**: Invalid inputs and edge cases
3. **Authentication**: Protected endpoint access
4. **Performance**: Response times and load testing""",
                content_html="<p>HTML content would be generated here...</p>",
                tags=["Testing", "FastAPI", "Python", "Quality Assurance"],
                published=False,  # Draft post
                featured=False,
                created_at=datetime(2024, 12, 5),
                published_at=None,
                reading_time_minutes=10,
                author="Brian Hardin",
                meta_description="Comprehensive guide to testing FastAPI applications with practical examples and best practices for robust, reliable code.",
                og_image="/static/images/blog/testing-fastapi-cover.jpg",
            ),
        ]


# Create a global instance
blog_service = BlogService()
