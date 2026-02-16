"""Adapters to convert SQLAlchemy DB models to Pydantic models for public routes."""

import json

from app.database.models import BlogPost as DBBlogPost
from app.database.models import Project as DBProject
from app.models.blog import BlogPost, BlogPostSummary
from app.models.project import (
    Project,
    ProjectCategory,
    ProjectOutcome,
    ProjectProblem,
    ProjectSolution,
    ProjectStatus,
    ProjectTimeline,
)


def db_blog_to_pydantic(post: DBBlogPost) -> BlogPost:
    """Convert a DB BlogPost to a Pydantic BlogPost."""
    tags: list[str] = []
    try:
        tags = json.loads(post.tags)
    except (json.JSONDecodeError, TypeError):
        pass

    return BlogPost(
        id=post.id,
        title=post.title,
        slug=post.slug,
        excerpt=post.excerpt,
        content=post.content,
        content_html=post.content_html,
        tags=tags,
        published=post.published,
        featured=post.featured,
        created_at=post.created_at,
        published_at=post.published_at,
        reading_time_minutes=post.reading_time_minutes,
        author=post.author,
        meta_description=post.meta_description,
    )


def db_blog_to_summary(post: DBBlogPost) -> BlogPostSummary:
    """Convert a DB BlogPost to a Pydantic BlogPostSummary."""
    tags: list[str] = []
    try:
        tags = json.loads(post.tags)
    except (json.JSONDecodeError, TypeError):
        pass

    return BlogPostSummary(
        id=post.id,
        title=post.title,
        slug=post.slug,
        excerpt=post.excerpt,
        tags=tags,
        published=post.published,
        featured=post.featured,
        created_at=post.created_at,
        published_at=post.published_at,
        reading_time_minutes=post.reading_time_minutes,
        author=post.author,
    )


def _parse_json(data: str, default: object = None) -> object:
    """Safely parse JSON string."""
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return default


def db_project_to_pydantic(proj: DBProject) -> Project:
    """Convert a DB Project to a Pydantic Project."""
    problem_data = _parse_json(proj.problem_json)
    solution_data = _parse_json(proj.solution_json)
    outcome_data = _parse_json(proj.outcome_json)
    timeline_data = _parse_json(proj.timeline_json, [])

    problem = None
    if isinstance(problem_data, dict) and problem_data.get("title"):
        problem = ProjectProblem(**problem_data)

    solution = None
    if isinstance(solution_data, dict) and solution_data.get("approach"):
        solution = ProjectSolution(**solution_data)

    outcome = None
    if isinstance(outcome_data, dict) and outcome_data.get("summary"):
        outcome = ProjectOutcome(**outcome_data)

    timeline = None
    if isinstance(timeline_data, list) and timeline_data:
        timeline = [ProjectTimeline(**t) for t in timeline_data]

    technologies: list[str] = []
    try:
        technologies = json.loads(proj.technologies)
    except (json.JSONDecodeError, TypeError):
        pass

    features: list[str] = []
    try:
        features = json.loads(proj.features)
    except (json.JSONDecodeError, TypeError):
        pass

    challenges: list[str] = []
    try:
        challenges = json.loads(proj.challenges)
    except (json.JSONDecodeError, TypeError):
        pass

    return Project(
        id=proj.id,
        title=proj.title,
        description=proj.description,
        long_description=proj.long_description or None,
        technologies=technologies,
        category=ProjectCategory(proj.category),
        status=ProjectStatus(proj.status),
        github_url=proj.github_url or None,
        demo_url=proj.demo_url or None,
        image_url=proj.image_url or None,
        duration=proj.duration or None,
        role=proj.role or None,
        featured=proj.featured,
        features=features,
        challenges=challenges,
        problem=problem,
        solution=solution,
        outcome=outcome,
        timeline=timeline,
        team_size=proj.team_size or None,
        client_type=proj.client_type or None,
    )
