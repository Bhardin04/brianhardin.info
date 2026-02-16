import logging

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import HTMLResponse

from app.models.contact import ContactForm
from app.models.project import Project
from app.services.email import email_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/projects")
async def get_projects() -> list[Project]:
    return [
        Project(
            id=1,
            title="Personal Brand Website",
            description="Modern responsive website built with FastAPI, featuring HTMX-powered contact forms, comprehensive testing with Puppeteer, and mobile-first design. Includes email integration and professional portfolio showcase.",
            technologies=[
                "Python",
                "FastAPI",
                "HTMX",
                "Tailwind CSS",
                "Puppeteer",
                "Docker",
            ],
            github_url="https://github.com/Bhardin04/brianhardin.info",
            demo_url="https://brianhardin.info",
        ),
        Project(
            id=2,
            title="API Documentation System",
            description="Automated API documentation generator for FastAPI applications with interactive testing capabilities, OpenAPI integration, and team collaboration features.",
            technologies=["Python", "FastAPI", "OpenAPI", "Pydantic", "PostgreSQL"],
            github_url="https://github.com/Bhardin04/api-docs-generator",
            demo_url="https://api-docs.brianhardin.info",
        ),
        Project(
            id=3,
            title="Data Pipeline Orchestrator",
            description="Scalable data processing pipeline built with async Python, featuring real-time monitoring, error handling, and integration with cloud storage services.",
            technologies=[
                "Python",
                "Asyncio",
                "Redis",
                "PostgreSQL",
                "Docker",
                "AWS S3",
            ],
            github_url="https://github.com/Bhardin04/data-pipeline",
            demo_url=None,
        ),
        Project(
            id=4,
            title="Microservices Auth System",
            description="JWT-based authentication microservice with role-based access control, rate limiting, and integration with multiple client applications.",
            technologies=["Python", "FastAPI", "JWT", "Redis", "PostgreSQL", "Docker"],
            github_url="https://github.com/Bhardin04/auth-microservice",
            demo_url=None,
        ),
    ]


@router.get("/projects/{project_id}")
async def get_project(project_id: int) -> Project:
    projects = {
        1: Project(
            id=1,
            title="Personal Brand Website",
            description="Modern responsive website built with FastAPI, featuring HTMX-powered contact forms, comprehensive testing with Puppeteer, and mobile-first design. Includes email integration and professional portfolio showcase.",
            technologies=[
                "Python",
                "FastAPI",
                "HTMX",
                "Tailwind CSS",
                "Puppeteer",
                "Docker",
            ],
            github_url="https://github.com/Bhardin04/brianhardin.info",
            demo_url="https://brianhardin.info",
        ),
        2: Project(
            id=2,
            title="API Documentation System",
            description="Automated API documentation generator for FastAPI applications with interactive testing capabilities, OpenAPI integration, and team collaboration features.",
            technologies=["Python", "FastAPI", "OpenAPI", "Pydantic", "PostgreSQL"],
            github_url="https://github.com/Bhardin04/api-docs-generator",
            demo_url="https://api-docs.brianhardin.info",
        ),
        3: Project(
            id=3,
            title="Data Pipeline Orchestrator",
            description="Scalable data processing pipeline built with async Python, featuring real-time monitoring, error handling, and integration with cloud storage services.",
            technologies=[
                "Python",
                "Asyncio",
                "Redis",
                "PostgreSQL",
                "Docker",
                "AWS S3",
            ],
            github_url="https://github.com/Bhardin04/data-pipeline",
            demo_url=None,
        ),
        4: Project(
            id=4,
            title="Microservices Auth System",
            description="JWT-based authentication microservice with role-based access control, rate limiting, and integration with multiple client applications.",
            technologies=["Python", "FastAPI", "JWT", "Redis", "PostgreSQL", "Docker"],
            github_url="https://github.com/Bhardin04/auth-microservice",
            demo_url=None,
        ),
    }

    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    return projects[project_id]


@router.post("/contact", response_class=HTMLResponse)
async def submit_contact_form(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    company: str = Form(None),
) -> str:
    try:
        # Create contact form data
        contact_data = ContactForm(
            name=name,
            email=email,
            subject=subject,
            message=message,
            company=company if company else None,
        )

        # Send email
        success = await email_service.send_contact_email(contact_data)

        if success:
            return """
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                <strong>Success!</strong> Your message has been sent. I'll get back to you soon!
            </div>
            """
        else:
            return """
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                <strong>Error!</strong> There was a problem sending your message. Please try again or email me directly.
            </div>
            """

    except ValueError as e:
        # Log the actual error for debugging but don't expose details to user
        logger.warning(f"Contact form validation error: {str(e)}")
        return """
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <strong>Error!</strong> Please check your input and try again.
        </div>
        """
    except Exception as e:
        # Log the actual error for debugging but don't expose details to user
        logger.error(f"Unexpected error in contact form: {str(e)}")
        return """
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <strong>Error!</strong> An unexpected error occurred. Please try again later.
        </div>
        """

@router.post("/analytics")
async def track_analytics(data: dict):
    """Analytics tracking endpoint - accepts analytics data but doesn't store it"""
    logger.info(f"Analytics tracked: {data}")
    return {"status": "tracked"}

@router.post("/error-report") 
async def report_error(error_data: dict):
    """Error reporting endpoint - logs errors for debugging"""
    logger.error(f"Client error reported: {error_data}")
    return {"status": "reported"}

@router.head("/ping")
@router.get("/ping")
async def ping():
    """Health check ping endpoint"""
    return {"status": "pong"}

@router.head("/health")
@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
