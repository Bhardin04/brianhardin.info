"""Database-backed project service with CRUD operations."""

import json
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Project

logger = logging.getLogger(__name__)


def _parse_json_list(data: str) -> list[str]:
    """Parse a JSON string into a list of strings."""
    try:
        result: list[str] = json.loads(data)
        return result
    except (json.JSONDecodeError, TypeError):
        return []


def _parse_json_dict(data: str) -> dict[str, object]:
    """Parse a JSON string into a dict."""
    try:
        result: dict[str, object] = json.loads(data)
        return result
    except (json.JSONDecodeError, TypeError):
        return {}


class ProjectServiceDB:
    """Database-backed project service."""

    async def get_all(self, db: AsyncSession) -> list[Project]:
        result = await db.execute(
            select(Project).order_by(Project.sort_order, Project.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, project_id: int) -> Project | None:
        result = await db.execute(select(Project).where(Project.id == project_id))
        row: Project | None = result.scalar_one_or_none()
        return row

    async def create(
        self,
        db: AsyncSession,
        *,
        title: str,
        description: str = "",
        long_description: str = "",
        technologies: list[str] | None = None,
        category: str = "web_app",
        status: str = "completed",
        featured: bool = False,
        sort_order: int = 0,
        image_url: str = "",
        github_url: str = "",
        demo_url: str = "",
        duration: str = "",
        role: str = "",
        team_size: str = "",
        client_type: str = "",
        features: list[str] | None = None,
        challenges: list[str] | None = None,
        problem_json: str = "{}",
        solution_json: str = "{}",
        outcome_json: str = "{}",
        timeline_json: str = "[]",
    ) -> Project:
        project = Project(
            title=title,
            description=description,
            long_description=long_description,
            technologies=json.dumps(technologies or []),
            category=category,
            status=status,
            featured=featured,
            sort_order=sort_order,
            image_url=image_url,
            github_url=github_url,
            demo_url=demo_url,
            duration=duration,
            role=role,
            team_size=team_size,
            client_type=client_type,
            features=json.dumps(features or []),
            challenges=json.dumps(challenges or []),
            problem_json=problem_json,
            solution_json=solution_json,
            outcome_json=outcome_json,
            timeline_json=timeline_json,
        )
        db.add(project)
        await db.flush()
        await db.commit()
        return project

    async def update(
        self,
        db: AsyncSession,
        project: Project,
        *,
        title: str,
        description: str = "",
        long_description: str = "",
        technologies: list[str] | None = None,
        category: str = "web_app",
        status: str = "completed",
        featured: bool = False,
        sort_order: int = 0,
        image_url: str = "",
        github_url: str = "",
        demo_url: str = "",
        duration: str = "",
        role: str = "",
        team_size: str = "",
        client_type: str = "",
        features: list[str] | None = None,
        challenges: list[str] | None = None,
        problem_json: str = "{}",
        solution_json: str = "{}",
        outcome_json: str = "{}",
        timeline_json: str = "[]",
    ) -> Project:
        project.title = title
        project.description = description
        project.long_description = long_description
        project.technologies = json.dumps(technologies or [])
        project.category = category
        project.status = status
        project.featured = featured
        project.sort_order = sort_order
        project.image_url = image_url
        project.github_url = github_url
        project.demo_url = demo_url
        project.duration = duration
        project.role = role
        project.team_size = team_size
        project.client_type = client_type
        project.features = json.dumps(features or [])
        project.challenges = json.dumps(challenges or [])
        project.problem_json = problem_json
        project.solution_json = solution_json
        project.outcome_json = outcome_json
        project.timeline_json = timeline_json

        await db.commit()
        return project

    async def delete(self, db: AsyncSession, project: Project) -> None:
        await db.delete(project)
        await db.commit()

    async def count(self, db: AsyncSession) -> int:
        result = await db.execute(select(Project.id))
        return len(result.all())


project_service_db = ProjectServiceDB()
