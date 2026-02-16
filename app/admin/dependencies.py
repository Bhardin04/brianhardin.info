"""Admin authentication dependency."""

import logging
from datetime import UTC, datetime

from fastapi import Cookie, HTTPException, Request
from sqlalchemy import select

from app.database.connection import get_db
from app.database.models import AdminSession

logger = logging.getLogger(__name__)


async def require_admin(
    request: Request,
    admin_session: str | None = Cookie(None),
) -> AdminSession:
    """FastAPI dependency that validates admin session cookie.

    Returns the AdminSession if valid, raises 401 otherwise.
    """
    if not admin_session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    async for db in get_db():
        result = await db.execute(
            select(AdminSession).where(AdminSession.session_token == admin_session)
        )
        row: AdminSession | None = result.scalar_one_or_none()

        if row is None:
            raise HTTPException(status_code=401, detail="Invalid session")

        now = datetime.now(UTC).replace(tzinfo=None)
        if row.expires_at.replace(tzinfo=None) < now:
            await db.delete(row)
            await db.commit()
            raise HTTPException(status_code=401, detail="Session expired")

        return row

    raise HTTPException(status_code=401, detail="Not authenticated")
