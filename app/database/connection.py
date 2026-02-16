import logging
import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

logger = logging.getLogger(__name__)

_engine = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def _get_engine_url() -> str:
    url = settings.DATABASE_URL
    # Render provides postgresql:// but SQLAlchemy async needs postgresql+asyncpg://
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


def _is_sqlite(url: str) -> bool:
    return url.startswith("sqlite")


async def init_db() -> None:
    """Initialize database engine and create all tables."""
    global _engine, _session_factory

    from app.database.models import Base

    url = _get_engine_url()
    is_sqlite = _is_sqlite(url)

    connect_args: dict[str, object] = {}
    if is_sqlite:
        connect_args["check_same_thread"] = False
        # Ensure data directory exists for file-based SQLite
        if ":///" in url and ":memory:" not in url:
            db_path = url.split(":///", 1)[1]
            os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)

    _engine = create_async_engine(
        url,
        echo=settings.DEBUG,
        connect_args=connect_args,
    )
    _session_factory = async_sessionmaker(_engine, expire_on_commit=False)

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database initialized: %s", "SQLite" if is_sqlite else "PostgreSQL")


async def close_db() -> None:
    """Dispose of the database engine."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None
        logger.info("Database connection closed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a database session."""
    if _session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    async with _session_factory() as session:
        yield session
