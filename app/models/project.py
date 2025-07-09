from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

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
    performance_improvement: Optional[str] = None
    user_engagement: Optional[str] = None
    cost_savings: Optional[str] = None
    efficiency_gains: Optional[str] = None
    scalability: Optional[str] = None
    uptime: Optional[str] = None
    response_time: Optional[str] = None
    user_satisfaction: Optional[str] = None


class ProjectProblem(BaseModel):
    """Problem statement and context"""
    title: str
    description: str
    pain_points: List[str]
    business_impact: str
    target_users: List[str]


class ProjectSolution(BaseModel):
    """Solution approach and implementation"""
    approach: str
    key_decisions: List[str]
    architecture: str
    implementation_highlights: List[str]


class ProjectOutcome(BaseModel):
    """Results and business impact"""
    summary: str
    achievements: List[str]
    metrics: ProjectMetrics
    user_feedback: List[str] = []
    lessons_learned: List[str] = []


class ProjectTimeline(BaseModel):
    """Project development timeline"""
    phase: str
    duration: str
    activities: List[str]
    deliverables: List[str]


class Project(BaseModel):
    id: int
    title: str
    description: str
    long_description: str | None = None
    technologies: list[str]
    category: ProjectCategory = ProjectCategory.WEB_APP
    status: ProjectStatus = ProjectStatus.COMPLETED
    github_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None
    image_url: str | None = None
    created_at: datetime | None = None
    duration: str | None = None
    role: str | None = None
    featured: bool = False
    challenges: list[str] = []
    features: list[str] = []
    
    # Enhanced case study fields
    problem: Optional[ProjectProblem] = None
    solution: Optional[ProjectSolution] = None
    outcome: Optional[ProjectOutcome] = None
    timeline: Optional[List[ProjectTimeline]] = None
    team_size: Optional[str] = None
    client_type: Optional[str] = None
    
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
    demo_url: HttpUrl | None = None
    image_url: str | None = None
    duration: str | None = None
    role: str | None = None
    featured: bool = False
    challenges: list[str] = []
    features: list[str] = []
