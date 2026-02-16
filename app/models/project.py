from datetime import datetime
from enum import Enum

from pydantic import BaseModel, HttpUrl


class ProjectCategory(str, Enum):
    WEB_APP = "web_app"
    API = "api"
    DATA_SCIENCE = "data_science"
    AUTOMATION = "automation"
    PERSONAL = "personal"
    OPEN_SOURCE = "open_source"


class ProjectStatus(str, Enum):
    COMPLETED = "completed"
    IN_PROGRESS = "in_progress"
    PLANNING = "planning"
    MAINTENANCE = "maintenance"


class ProjectMetrics(BaseModel):
    """Business and technical metrics for project impact"""
    performance_improvement: str | None = None
    user_engagement: str | None = None
    cost_savings: str | None = None
    efficiency_gains: str | None = None
    scalability: str | None = None
    uptime: str | None = None
    response_time: str | None = None
    user_satisfaction: str | None = None


class ProjectProblem(BaseModel):
    """Problem statement and context"""
    title: str
    description: str
    pain_points: list[str]
    business_impact: str
    target_users: list[str]


class ProjectSolution(BaseModel):
    """Solution approach and implementation"""
    approach: str
    key_decisions: list[str]
    architecture: str
    implementation_highlights: list[str]


class ProjectOutcome(BaseModel):
    """Results and business impact"""
    summary: str
    achievements: list[str]
    metrics: ProjectMetrics
    user_feedback: list[str] = []
    lessons_learned: list[str] = []


class ProjectTimeline(BaseModel):
    """Project development timeline"""
    phase: str
    duration: str
    activities: list[str]
    deliverables: list[str]


class Project(BaseModel):
    id: int
    title: str
    description: str
    long_description: str | None = None
    technologies: list[str]
    category: ProjectCategory = ProjectCategory.WEB_APP
    status: ProjectStatus = ProjectStatus.COMPLETED
    github_url: HttpUrl | None = None
    demo_url: str | None = None
    image_url: str | None = None
    created_at: datetime | None = None
    duration: str | None = None
    role: str | None = None
    featured: bool = False
    challenges: list[str] = []
    features: list[str] = []

    # Enhanced case study fields
    problem: ProjectProblem | None = None
    solution: ProjectSolution | None = None
    outcome: ProjectOutcome | None = None
    timeline: list[ProjectTimeline] | None = None
    team_size: str | None = None
    client_type: str | None = None

    class Config:
        use_enum_values = True


class ProjectCreate(BaseModel):
    title: str
    description: str
    long_description: str | None = None
    technologies: list[str]
    category: ProjectCategory = ProjectCategory.WEB_APP
    status: ProjectStatus = ProjectStatus.COMPLETED
    github_url: HttpUrl | None = None
    demo_url: str | None = None
    image_url: str | None = None
    duration: str | None = None
    role: str | None = None
    featured: bool = False
    challenges: list[str] = []
    features: list[str] = []
