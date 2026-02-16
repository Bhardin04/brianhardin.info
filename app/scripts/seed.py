"""Seed script to migrate hardcoded data into the database.

Usage:
    python -m app.scripts.seed
"""

import asyncio
import json
import logging
import sys

from sqlalchemy import select

from app.database.connection import get_db, init_db
from app.database.models import BlogPost as DBBlogPost
from app.database.models import Project as DBProject
from app.services.blog import blog_service
from app.services.blog_db import render_markdown
from app.services.project import project_service

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


async def seed_blog_posts() -> int:
    """Seed blog posts from the hardcoded sample data."""
    posts = blog_service.get_all_posts(published_only=False)
    count = 0

    async for db in get_db():
        for post in posts:
            # Check if already seeded (by slug)
            result = await db.execute(
                select(DBBlogPost).where(DBBlogPost.slug == post.slug)
            )
            if result.scalar_one_or_none():
                logger.info("  Blog post '%s' already exists, skipping", post.title)
                continue

            content_html = render_markdown(post.content)

            db_post = DBBlogPost(
                title=post.title,
                slug=post.slug,
                content=post.content,
                content_html=content_html,
                excerpt=post.excerpt,
                tags=json.dumps(post.tags),
                published=post.published,
                featured=post.featured,
                author=post.author,
                meta_description=post.meta_description or "",
                reading_time_minutes=post.reading_time_minutes or 1,
            )
            db.add(db_post)
            count += 1
            logger.info("  Seeded blog post: %s", post.title)

        await db.commit()

    return count


async def seed_projects() -> int:
    """Seed projects from the hardcoded project data."""
    projects = project_service.get_all()
    count = 0

    async for db in get_db():
        for proj in projects:
            # Check if already seeded (by title)
            result = await db.execute(
                select(DBProject).where(DBProject.title == proj.title)
            )
            if result.scalar_one_or_none():
                logger.info("  Project '%s' already exists, skipping", proj.title)
                continue

            db_proj = DBProject(
                title=proj.title,
                description=proj.description,
                long_description=proj.long_description or "",
                technologies=json.dumps(proj.technologies),
                category=proj.category
                if isinstance(proj.category, str)
                else proj.category.value,
                status=proj.status
                if isinstance(proj.status, str)
                else proj.status.value,
                featured=proj.featured,
                sort_order=0,
                image_url=proj.image_url or "",
                github_url=proj.github_url or "",
                demo_url=proj.demo_url or "",
                duration=proj.duration or "",
                role=proj.role or "",
                team_size=proj.team_size or "",
                client_type=proj.client_type or "",
                features=json.dumps(proj.features),
                challenges=json.dumps(proj.challenges),
                problem_json=proj.problem.model_dump_json() if proj.problem else "{}",
                solution_json=proj.solution.model_dump_json()
                if proj.solution
                else "{}",
                outcome_json=proj.outcome.model_dump_json() if proj.outcome else "{}",
                timeline_json=json.dumps(
                    [t.model_dump() for t in proj.timeline] if proj.timeline else []
                ),
            )
            db.add(db_proj)
            count += 1
            logger.info("  Seeded project: %s", proj.title)

        await db.commit()

    return count


async def main() -> None:
    """Run the seed script."""
    logger.info("Initializing database...")
    await init_db()

    logger.info("Seeding blog posts...")
    blog_count = await seed_blog_posts()
    logger.info("Seeded %d blog posts", blog_count)

    logger.info("Seeding projects...")
    project_count = await seed_projects()
    logger.info("Seeded %d projects", project_count)

    logger.info("Done! Seeded %d total items.", blog_count + project_count)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
