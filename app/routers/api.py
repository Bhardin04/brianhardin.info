from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import HTMLResponse
from app.models.project import Project
from app.models.contact import ContactForm, ContactResponse
from app.services.email import email_service

router = APIRouter()

@router.get("/projects")
async def get_projects():
    return [
        Project(
            id=1,
            title="Personal Website",
            description="FastAPI-based personal brand website",
            technologies=["Python", "FastAPI", "Jinja2", "HTMX"],
            github_url="https://github.com/Bhardin04/brianhardin.info",
            demo_url="https://brianhardin.info"
        )
    ]

@router.get("/projects/{project_id}")
async def get_project(project_id: int):
    return Project(
        id=project_id,
        title="Project Details",
        description="Detailed view of the project",
        technologies=["Python", "FastAPI"],
        github_url="https://github.com/example",
        demo_url="https://example.com"
    )

@router.post("/contact", response_class=HTMLResponse)
async def submit_contact_form(
    name: str = Form(...),
    email: str = Form(...),
    subject: str = Form(...),
    message: str = Form(...),
    company: str = Form(None)
):
    try:
        # Create contact form data
        contact_data = ContactForm(
            name=name,
            email=email,
            subject=subject,
            message=message,
            company=company if company else None
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
        return f"""
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <strong>Error!</strong> {str(e)}
        </div>
        """
    except Exception as e:
        return """
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <strong>Error!</strong> An unexpected error occurred. Please try again later.
        </div>
        """