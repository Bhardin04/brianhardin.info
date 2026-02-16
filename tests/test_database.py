"""Tests for database service layer, adapters, and seed script."""

import json

import pytest

from app.database.connection import get_db, init_db
from app.database.models import BlogPost as DBBlogPost
from app.database.models import Project as DBProject
from app.services.blog_db import (
    blog_service_db,
    calculate_reading_time,
    render_markdown,
)
from app.services.db_adapters import (
    db_blog_to_pydantic,
    db_blog_to_summary,
    db_project_to_pydantic,
)
from app.services.project_db import project_service_db


@pytest.fixture(autouse=True)
async def setup_db(monkeypatch):
    """Use in-memory SQLite for tests."""
    monkeypatch.setattr(
        "app.database.connection.settings",
        type(
            "S",
            (),
            {"DATABASE_URL": "sqlite+aiosqlite:///:memory:", "DEBUG": False},
        )(),
    )
    await init_db()
    yield


class TestBlogServiceDB:
    async def test_create_blog_post(self):
        async for db in get_db():
            post = await blog_service_db.create(
                db,
                title="Test Post",
                slug="test-post",
                excerpt="A test excerpt",
                content="# Hello\n\nSome content here.",
                tags=["Python", "Testing"],
                published=True,
                featured=False,
            )
            assert post.id is not None
            assert post.title == "Test Post"
            assert post.slug == "test-post"
            assert post.published is True

    async def test_get_all_published(self):
        async for db in get_db():
            await blog_service_db.create(
                db,
                title="Published",
                slug="published",
                excerpt="Published post",
                content="Content",
                published=True,
            )
            await blog_service_db.create(
                db,
                title="Draft",
                slug="draft",
                excerpt="Draft post",
                content="Content",
                published=False,
            )

            published = await blog_service_db.get_all(db, published_only=True)
            assert len(published) == 1
            assert published[0].title == "Published"

            all_posts = await blog_service_db.get_all(db, published_only=False)
            assert len(all_posts) == 2

    async def test_get_by_slug(self):
        async for db in get_db():
            await blog_service_db.create(
                db,
                title="Slug Test",
                slug="slug-test",
                excerpt="Testing slug lookup",
                content="Content",
            )
            found = await blog_service_db.get_by_slug(db, "slug-test")
            assert found is not None
            assert found.title == "Slug Test"

            missing = await blog_service_db.get_by_slug(db, "nonexistent")
            assert missing is None

    async def test_update_blog_post(self):
        async for db in get_db():
            post = await blog_service_db.create(
                db,
                title="Original",
                slug="original",
                excerpt="Original excerpt",
                content="Original content",
            )
            updated = await blog_service_db.update(
                db,
                post,
                title="Updated Title",
                slug="updated-title",
                excerpt="Updated excerpt",
                content="Updated content",
                tags=["updated"],
                published=True,
                featured=True,
            )
            assert updated.title == "Updated Title"
            assert updated.published is True

    async def test_delete_blog_post(self):
        async for db in get_db():
            post = await blog_service_db.create(
                db,
                title="To Delete",
                slug="to-delete",
                excerpt="Will be deleted",
                content="Content",
            )
            post_id = post.id
            await blog_service_db.delete(db, post)

            result = await blog_service_db.get_by_id(db, post_id)
            assert result is None

    async def test_toggle_publish(self):
        async for db in get_db():
            post = await blog_service_db.create(
                db,
                title="Toggle Test",
                slug="toggle-test",
                excerpt="Toggle publish",
                content="Content",
                published=False,
            )
            assert post.published is False

            toggled = await blog_service_db.toggle_publish(db, post)
            assert toggled.published is True

    async def test_count(self):
        async for db in get_db():
            assert await blog_service_db.count(db) == 0
            await blog_service_db.create(
                db,
                title="Post 1",
                slug="post-1",
                excerpt="Excerpt",
                content="Content",
            )
            assert await blog_service_db.count(db) == 1


class TestProjectServiceDB:
    async def test_create_project(self):
        async for db in get_db():
            project = await project_service_db.create(
                db,
                title="Test Project",
                description="A test project",
                technologies=["Python", "FastAPI"],
                category="web_app",
                status="completed",
                featured=True,
            )
            assert project.id is not None
            assert project.title == "Test Project"
            assert project.featured is True

    async def test_get_all_projects(self):
        async for db in get_db():
            await project_service_db.create(db, title="Project A", description="A")
            await project_service_db.create(db, title="Project B", description="B")

            projects = await project_service_db.get_all(db)
            assert len(projects) == 2

    async def test_get_by_id(self):
        async for db in get_db():
            project = await project_service_db.create(
                db, title="Find Me", description="Findable"
            )
            found = await project_service_db.get_by_id(db, project.id)
            assert found is not None
            assert found.title == "Find Me"

            missing = await project_service_db.get_by_id(db, 9999)
            assert missing is None

    async def test_update_project(self):
        async for db in get_db():
            project = await project_service_db.create(
                db, title="Original", description="Original desc"
            )
            updated = await project_service_db.update(
                db,
                project,
                title="Updated",
                description="Updated desc",
                technologies=["Python"],
                featured=True,
            )
            assert updated.title == "Updated"
            assert updated.featured is True

    async def test_delete_project(self):
        async for db in get_db():
            project = await project_service_db.create(
                db, title="To Delete", description="Will be deleted"
            )
            pid = project.id
            await project_service_db.delete(db, project)

            result = await project_service_db.get_by_id(db, pid)
            assert result is None

    async def test_json_roundtrip(self):
        """Test that JSON fields serialize and deserialize correctly."""
        async for db in get_db():
            techs = ["Python", "FastAPI", "PostgreSQL"]
            features = ["Feature 1", "Feature 2"]
            challenges = ["Challenge 1"]
            problem_json = json.dumps(
                {
                    "title": "Test Problem",
                    "description": "Problem desc",
                    "pain_points": ["Pain 1"],
                    "business_impact": "High",
                    "target_users": ["User 1"],
                }
            )
            solution_json = json.dumps(
                {
                    "approach": "Test approach",
                    "key_decisions": ["Decision 1"],
                    "architecture": "Test arch",
                    "implementation_highlights": ["Highlight 1"],
                }
            )
            outcome_json = json.dumps(
                {
                    "summary": "Test outcome",
                    "achievements": ["Achievement 1"],
                    "metrics": {},
                    "user_feedback": ["Feedback 1"],
                    "lessons_learned": ["Lesson 1"],
                }
            )
            timeline_json = json.dumps(
                [
                    {
                        "phase": "Phase 1",
                        "duration": "1 week",
                        "activities": ["Activity 1"],
                        "deliverables": ["Deliverable 1"],
                    }
                ]
            )

            project = await project_service_db.create(
                db,
                title="JSON Test",
                description="JSON roundtrip test",
                technologies=techs,
                features=features,
                challenges=challenges,
                problem_json=problem_json,
                solution_json=solution_json,
                outcome_json=outcome_json,
                timeline_json=timeline_json,
            )

            # Convert to Pydantic and verify
            pydantic_proj = db_project_to_pydantic(project)
            assert pydantic_proj.technologies == techs
            assert pydantic_proj.features == features
            assert pydantic_proj.challenges == challenges
            assert pydantic_proj.problem is not None
            assert pydantic_proj.problem.title == "Test Problem"
            assert pydantic_proj.solution is not None
            assert pydantic_proj.solution.approach == "Test approach"
            assert pydantic_proj.outcome is not None
            assert pydantic_proj.outcome.summary == "Test outcome"
            assert pydantic_proj.timeline is not None
            assert len(pydantic_proj.timeline) == 1
            assert pydantic_proj.timeline[0].phase == "Phase 1"


class TestDBAdapters:
    async def test_blog_to_pydantic(self):
        async for db in get_db():
            db_post = DBBlogPost(
                title="Adapter Test",
                slug="adapter-test",
                content="# Test",
                content_html="<h1>Test</h1>",
                excerpt="Adapter test",
                tags=json.dumps(["Python", "Testing"]),
                published=True,
                featured=False,
                author="Brian Hardin",
                meta_description="Adapter desc",
                reading_time_minutes=2,
            )
            db.add(db_post)
            await db.flush()

            pydantic_post = db_blog_to_pydantic(db_post)
            assert pydantic_post.title == "Adapter Test"
            assert pydantic_post.tags == ["Python", "Testing"]
            assert pydantic_post.published is True
            assert pydantic_post.reading_time_minutes == 2

    async def test_blog_to_summary(self):
        async for db in get_db():
            db_post = DBBlogPost(
                title="Summary Test",
                slug="summary-test",
                content="Content",
                content_html="<p>Content</p>",
                excerpt="Summary excerpt",
                tags=json.dumps(["Python"]),
                published=True,
                featured=True,
                author="Brian Hardin",
                meta_description="",
                reading_time_minutes=1,
            )
            db.add(db_post)
            await db.flush()

            summary = db_blog_to_summary(db_post)
            assert summary.title == "Summary Test"
            assert summary.tags == ["Python"]
            assert summary.featured is True
            # Summary should NOT have content or content_html
            assert (
                not hasattr(summary, "content") or "content" not in summary.model_fields
            )

    async def test_blog_invalid_tags_json(self):
        async for db in get_db():
            db_post = DBBlogPost(
                title="Bad Tags",
                slug="bad-tags",
                content="Content",
                content_html="<p>Content</p>",
                excerpt="Bad tags test",
                tags="not valid json",
                published=True,
                featured=False,
                author="Brian Hardin",
                meta_description="",
                reading_time_minutes=1,
            )
            db.add(db_post)
            await db.flush()

            pydantic_post = db_blog_to_pydantic(db_post)
            assert pydantic_post.tags == []

    async def test_project_to_pydantic_minimal(self):
        """Test project adapter with minimal data (no case study)."""
        async for db in get_db():
            db_proj = DBProject(
                title="Minimal Project",
                description="Minimal desc",
                long_description="",
                technologies=json.dumps(["Python"]),
                category="web_app",
                status="completed",
                featured=False,
                sort_order=0,
                image_url="",
                github_url="",
                demo_url="",
                duration="",
                role="",
                team_size="",
                client_type="",
                features=json.dumps([]),
                challenges=json.dumps([]),
                problem_json="{}",
                solution_json="{}",
                outcome_json="{}",
                timeline_json="[]",
            )
            db.add(db_proj)
            await db.flush()

            pydantic_proj = db_project_to_pydantic(db_proj)
            assert pydantic_proj.title == "Minimal Project"
            assert pydantic_proj.technologies == ["Python"]
            assert pydantic_proj.problem is None
            assert pydantic_proj.solution is None
            assert pydantic_proj.outcome is None
            assert pydantic_proj.timeline is None


class TestUtilities:
    def test_calculate_reading_time(self):
        # ~200 words = 1 minute
        short_content = "word " * 50
        assert calculate_reading_time(short_content) == 1

        # ~600 words = 3 minutes
        long_content = "word " * 600
        assert calculate_reading_time(long_content) == 3

    def test_render_markdown(self):
        md = "# Hello\n\nThis is **bold** text."
        result = render_markdown(md)
        assert "<h1" in result
        assert "<strong>bold</strong>" in result


class TestSeedScript:
    async def test_seed_blog_posts(self):
        from app.scripts.seed import seed_blog_posts

        count = await seed_blog_posts()
        assert count > 0

        # Verify posts exist in database
        async for db in get_db():
            total = await blog_service_db.count(db)
            assert total == count

    async def test_seed_blog_posts_idempotent(self):
        from app.scripts.seed import seed_blog_posts

        count1 = await seed_blog_posts()
        count2 = await seed_blog_posts()
        assert count1 > 0
        assert count2 == 0  # Second run should skip all

    async def test_seed_projects(self):
        from app.scripts.seed import seed_projects

        count = await seed_projects()
        assert count > 0

        async for db in get_db():
            total = await project_service_db.count(db)
            assert total == count

    async def test_seed_projects_idempotent(self):
        from app.scripts.seed import seed_projects

        count1 = await seed_projects()
        count2 = await seed_projects()
        assert count1 > 0
        assert count2 == 0
