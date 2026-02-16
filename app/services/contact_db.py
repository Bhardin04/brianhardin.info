"""Database-backed contact message service."""

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import ContactMessage

logger = logging.getLogger(__name__)


class ContactMessageService:
    """CRUD operations for contact messages."""

    async def get_all(
        self,
        db: AsyncSession,
        *,
        unread_only: bool = False,
        archived: bool = False,
    ) -> list[ContactMessage]:
        stmt = (
            select(ContactMessage)
            .where(ContactMessage.archived == archived)  # noqa: E712
            .order_by(ContactMessage.created_at.desc())
        )
        if unread_only:
            stmt = stmt.where(ContactMessage.read == False)  # noqa: E712
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(
        self, db: AsyncSession, message_id: int
    ) -> ContactMessage | None:
        result = await db.execute(
            select(ContactMessage).where(ContactMessage.id == message_id)
        )
        row: ContactMessage | None = result.scalar_one_or_none()
        return row

    async def create(
        self,
        db: AsyncSession,
        *,
        name: str,
        email: str,
        subject: str = "",
        message: str,
        company: str = "",
    ) -> ContactMessage:
        msg = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message,
            company=company,
        )
        db.add(msg)
        await db.flush()
        await db.commit()
        return msg

    async def mark_read(self, db: AsyncSession, msg: ContactMessage) -> None:
        msg.read = True
        await db.commit()

    async def toggle_archive(self, db: AsyncSession, msg: ContactMessage) -> None:
        msg.archived = not msg.archived
        await db.commit()

    async def delete(self, db: AsyncSession, msg: ContactMessage) -> None:
        await db.delete(msg)
        await db.commit()

    async def unread_count(self, db: AsyncSession) -> int:
        from sqlalchemy import func

        result = await db.execute(
            select(func.count(ContactMessage.id)).where(
                ContactMessage.read == False,  # noqa: E712
                ContactMessage.archived == False,  # noqa: E712
            )
        )
        return result.scalar() or 0


contact_message_service = ContactMessageService()
