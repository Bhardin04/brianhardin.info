from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    company: Optional[str] = None

class ContactResponse(BaseModel):
    success: bool
    message: str