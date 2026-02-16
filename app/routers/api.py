import logging

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.database.connection import get_db
from app.middleware import limiter, verify_csrf_token
from app.models.contact import ContactForm
from app.models.project import Project
from app.services.contact_db import contact_message_service
from app.services.email import email_service
from app.services.project import project_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/projects")
async def get_projects() -> list[Project]:
    return project_service.get_all()


@router.get("/projects/{project_id}")
async def get_project(project_id: int) -> Project:
    project = project_service.get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/contact", response_class=HTMLResponse)
@limiter.limit("1/minute")
@limiter.limit("3/hour")
async def submit_contact_form(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    company: str = Form(None),
    _csrf: None = Depends(verify_csrf_token),
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

        # Save to database
        try:
            async for db in get_db():
                await contact_message_service.create(
                    db,
                    name=contact_data.name,
                    email=contact_data.email,
                    subject=contact_data.subject,
                    message=contact_data.message,
                    company=contact_data.company or "",
                )
        except Exception:
            logger.exception("Failed to save contact message to database")

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
@limiter.limit("30/minute")
async def track_analytics(request: Request, data: dict[str, str]) -> dict[str, str]:
    """Analytics tracking endpoint - accepts analytics data but doesn't store it"""
    logger.info(f"Analytics tracked: {data}")
    return {"status": "tracked"}


@router.post("/error-report")
@limiter.limit("10/minute")
async def report_error(request: Request, error_data: dict[str, str]) -> dict[str, str]:
    """Error reporting endpoint - logs errors for debugging"""
    logger.error(f"Client error reported: {error_data}")
    return {"status": "reported"}


@router.head("/ping")
@router.get("/ping")
async def ping() -> dict[str, str]:
    """Health check ping endpoint"""
    return {"status": "pong"}


@router.head("/health")
@router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}
