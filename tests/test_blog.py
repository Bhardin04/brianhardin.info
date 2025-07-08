import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.blog import blog_service

client = TestClient(app)


class TestBlogRoutes:
    """Test blog routes and functionality."""

    def test_blog_index_page(self):
        """Test blog listing page loads correctly."""
        response = client.get("/blog")
        assert response.status_code == 200
        assert "Technical Blog" in response.text
        assert "Brian Hardin" in response.text

    def test_blog_post_page(self):
        """Test individual blog post page loads correctly."""
        response = client.get("/blog/fastapi-htmx-modern-web-apps")
        assert response.status_code == 200
        assert "Building Modern Web Applications with FastAPI and HTMX" in response.text

    def test_blog_post_not_found(self):
        """Test 404 for non-existent blog post."""
        response = client.get("/blog/non-existent-post")
        assert response.status_code == 404

    def test_blog_filter_by_tag(self):
        """Test filtering blog posts by tag."""
        response = client.get("/blog?tag=Python")
        assert response.status_code == 200
        assert "Python" in response.text

    def test_api_blog_posts(self):
        """Test blog posts API endpoint."""
        response = client.get("/api/blog/posts")
        assert response.status_code == 200
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) > 0
        
        # Check post structure
        post = posts[0]
        required_fields = ["id", "title", "slug", "excerpt", "tags", "published"]
        for field in required_fields:
            assert field in post

    def test_api_blog_post_detail(self):
        """Test individual blog post API endpoint."""
        response = client.get("/api/blog/posts/fastapi-htmx-modern-web-apps")
        assert response.status_code == 200
        post = response.json()
        assert post["title"] == "Building Modern Web Applications with FastAPI and HTMX"
        assert post["slug"] == "fastapi-htmx-modern-web-apps"

    def test_api_blog_post_not_found(self):
        """Test 404 for non-existent blog post via API."""
        response = client.get("/api/blog/posts/non-existent-post")
        assert response.status_code == 404

    def test_api_featured_posts(self):
        """Test featured posts API endpoint."""
        response = client.get("/api/blog/featured")
        assert response.status_code == 200
        posts = response.json()
        assert isinstance(posts, list)
        # All returned posts should be featured
        for post in posts:
            assert post["featured"] is True

    def test_api_blog_tags(self):
        """Test blog tags API endpoint."""
        response = client.get("/api/blog/tags")
        assert response.status_code == 200
        tags = response.json()
        assert isinstance(tags, list)
        assert "Python" in tags
        assert "FastAPI" in tags


class TestBlogService:
    """Test blog service functionality."""

    def test_get_all_posts(self):
        """Test getting all blog posts."""
        posts = blog_service.get_all_posts()
        assert len(posts) > 0
        assert all(post.published for post in posts)

    def test_get_all_posts_including_drafts(self):
        """Test getting all posts including drafts."""
        all_posts = blog_service.get_all_posts(published_only=False)
        published_posts = blog_service.get_all_posts(published_only=True)
        assert len(all_posts) >= len(published_posts)

    def test_get_posts_summary(self):
        """Test getting blog post summaries."""
        summaries = blog_service.get_posts_summary()
        assert len(summaries) > 0
        
        # Check summary structure
        summary = summaries[0]
        assert hasattr(summary, 'id')
        assert hasattr(summary, 'title')
        assert hasattr(summary, 'slug')
        assert hasattr(summary, 'excerpt')

    def test_get_post_by_slug(self):
        """Test getting a post by slug."""
        post = blog_service.get_post_by_slug("fastapi-htmx-modern-web-apps")
        assert post is not None
        assert post.title == "Building Modern Web Applications with FastAPI and HTMX"

    def test_get_post_by_slug_not_found(self):
        """Test getting non-existent post by slug."""
        post = blog_service.get_post_by_slug("non-existent-slug")
        assert post is None

    def test_get_post_by_id(self):
        """Test getting a post by ID."""
        post = blog_service.get_post_by_id(1)
        assert post is not None
        assert post.id == 1

    def test_get_featured_posts(self):
        """Test getting featured posts."""
        featured = blog_service.get_featured_posts()
        assert len(featured) > 0
        assert all(post.featured for post in featured)

    def test_get_posts_by_tag(self):
        """Test filtering posts by tag."""
        python_posts = blog_service.get_posts_by_tag("Python")
        assert len(python_posts) > 0
        assert all("Python" in post.tags for post in python_posts)

    def test_get_posts_by_tag_case_insensitive(self):
        """Test tag filtering is case insensitive."""
        python_posts = blog_service.get_posts_by_tag("python")
        assert len(python_posts) > 0

    def test_calculate_reading_time(self):
        """Test reading time calculation."""
        short_content = "This is a short piece of content."
        reading_time = blog_service._calculate_reading_time(short_content)
        assert reading_time == 1  # Minimum 1 minute

        long_content = " ".join(["word"] * 400)  # 400 words
        reading_time = blog_service._calculate_reading_time(long_content)
        assert reading_time == 2  # 400 words / 200 words per minute

    def test_generate_slug(self):
        """Test slug generation."""
        title = "Building Modern Web Applications with FastAPI and HTMX"
        slug = blog_service._generate_slug(title)
        assert slug == "building-modern-web-applications-with-fastapi-and-htmx"

    def test_generate_slug_with_special_chars(self):
        """Test slug generation with special characters."""
        title = "Python & FastAPI: A Developer's Guide (2024)"
        slug = blog_service._generate_slug(title)
        assert slug == "python-fastapi-a-developers-guide-2024"