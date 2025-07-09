import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from app.models.contact import ContactForm


class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_username)
        self.to_email = os.getenv("TO_EMAIL", "brian.hardin@icloud.com")

    async def send_contact_email(self, contact_data: ContactForm) -> bool:
        """Send contact form email"""
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Contact Form: {contact_data.subject}"
            message["From"] = self.from_email
            message["To"] = self.to_email
            message["Reply-To"] = contact_data.email

            # Create email content
            text_content = self._create_text_content(contact_data)
            html_content = self._create_html_content(contact_data)

            # Attach parts
            text_part = MIMEText(text_content, "plain")
            html_part = MIMEText(html_content, "html")

            message.attach(text_part)
            message.attach(html_part)

            # Send email
            if self.smtp_username and self.smtp_password:
                await aiosmtplib.send(
                    message,
                    hostname=self.smtp_server,
                    port=self.smtp_port,
                    start_tls=True,
                    username=self.smtp_username,
                    password=self.smtp_password,
                )
                return True
            else:
                # In development, just log the email
                print("=== EMAIL (Development Mode) ===")
                print(f"From: {contact_data.email}")
                print(f"Subject: {contact_data.subject}")
                print(f"Message: {contact_data.message}")
                print("================================")
                return True

        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    def _create_text_content(self, contact_data: ContactForm) -> str:
        """Create plain text email content"""
        company_info = f"\nCompany: {contact_data.company}" if contact_data.company else ""

        return f"""
New contact form submission from brianhardin.info

Name: {contact_data.name}
Email: {contact_data.email}{company_info}
Subject: {contact_data.subject}

Message:
{contact_data.message}

---
This message was sent from the contact form on brianhardin.info
        """.strip()

    def _create_html_content(self, contact_data: ContactForm) -> str:
        """Create HTML email content"""
        company_row = f"""
        <tr>
            <td style="padding: 8px 0; font-weight: bold;">Company:</td>
            <td style="padding: 8px 0;">{contact_data.company}</td>
        </tr>
        """ if contact_data.company else ""

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Contact Form Submission</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2563eb; border-bottom: 2px solid #2563eb; padding-bottom: 10px;">
                    New Contact Form Submission
                </h2>

                <table style="width: 100%; margin: 20px 0;">
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold;">Name:</td>
                        <td style="padding: 8px 0;">{contact_data.name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold;">Email:</td>
                        <td style="padding: 8px 0;">
                            <a href="mailto:{contact_data.email}">{contact_data.email}</a>
                        </td>
                    </tr>
                    {company_row}
                    <tr>
                        <td style="padding: 8px 0; font-weight: bold;">Subject:</td>
                        <td style="padding: 8px 0;">{contact_data.subject}</td>
                    </tr>
                </table>

                <div style="margin: 20px 0;">
                    <h3 style="color: #374151;">Message:</h3>
                    <div style="background: #f9fafb; padding: 15px; border-left: 4px solid #2563eb; margin: 10px 0;">
                        {contact_data.message.replace(chr(10), '<br>')}
                    </div>
                </div>

                <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 30px 0;">
                <p style="color: #6b7280; font-size: 14px;">
                    This message was sent from the contact form on
                    <a href="https://brianhardin.info" style="color: #2563eb;">brianhardin.info</a>
                </p>
            </div>
        </body>
        </html>
        """

# Create global email service instance
email_service = EmailService()
