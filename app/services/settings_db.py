"""Database-backed site settings service."""

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import SiteSetting

logger = logging.getLogger(__name__)


class SiteSettingsService:
    """Key-value settings stored in the database."""

    async def get(self, db: AsyncSession, key: str) -> str | None:
        result = await db.execute(select(SiteSetting).where(SiteSetting.key == key))
        row: SiteSetting | None = result.scalar_one_or_none()
        return row.value if row else None

    async def get_all(self, db: AsyncSession) -> dict[str, str]:
        result = await db.execute(select(SiteSetting))
        return {s.key: s.value for s in result.scalars().all()}

    async def set(self, db: AsyncSession, key: str, value: str) -> None:
        result = await db.execute(select(SiteSetting).where(SiteSetting.key == key))
        existing: SiteSetting | None = result.scalar_one_or_none()
        if existing:
            existing.value = value
        else:
            db.add(SiteSetting(key=key, value=value))
        await db.commit()

    async def set_many(self, db: AsyncSession, settings: dict[str, str]) -> None:
        for key, value in settings.items():
            result = await db.execute(select(SiteSetting).where(SiteSetting.key == key))
            existing: SiteSetting | None = result.scalar_one_or_none()
            if existing:
                existing.value = value
            else:
                db.add(SiteSetting(key=key, value=value))
        await db.commit()


site_settings_service = SiteSettingsService()
