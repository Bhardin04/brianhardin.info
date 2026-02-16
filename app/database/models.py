from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):  # type: ignore[misc]
    pass


class BlogPost(Base):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False, default="")
    content_html: Mapped[str] = mapped_column(Text, nullable=False, default="")
    excerpt: Mapped[str] = mapped_column(Text, nullable=False, default="")
    tags: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON array
    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    author: Mapped[str] = mapped_column(
        String(255), nullable=False, default="Brian Hardin"
    )
    meta_description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    reading_time_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    long_description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    technologies: Mapped[str] = mapped_column(
        Text, nullable=False, default="[]"
    )  # JSON
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="completed")
    featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    github_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    demo_url: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    duration: Mapped[str] = mapped_column(String(100), nullable=False, default="")
    role: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    team_size: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    client_type: Mapped[str] = mapped_column(String(100), nullable=False, default="")

    # Nested case study data stored as JSON text
    problem_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    solution_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    outcome_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    timeline_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    features: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON
    challenges: Mapped[str] = mapped_column(Text, nullable=False, default="[]")  # JSON

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )


class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(500), nullable=False, default="")
    message: Mapped[str] = mapped_column(Text, nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    archived: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )


class AdminSession(Base):
    __tablename__ = "admin_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_token: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    github_username: Mapped[str] = mapped_column(String(255), nullable=False)
    github_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class SiteSetting(Base):
    __tablename__ = "site_settings"

    key: Mapped[str] = mapped_column(String(255), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False, default="")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
