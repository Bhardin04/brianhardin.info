from pydantic import BaseModel, EmailStr, Field


class ContactForm(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Valid email address")
    subject: str = Field(
        ..., min_length=1, max_length=200, description="Message subject"
    )
    message: str = Field(
        ..., min_length=10, max_length=5000, description="Message content"
    )
    company: str | None = Field(
        None, max_length=100, description="Company name (optional)"
    )


class ContactResponse(BaseModel):
    success: bool
    message: str
