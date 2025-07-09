
from pydantic import BaseModel, EmailStr


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    company: str | None = None

class ContactResponse(BaseModel):
    success: bool
    message: str
