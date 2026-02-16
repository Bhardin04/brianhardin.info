# Contact Form Setup

The contact form is now fully functional with email sending capabilities.

## Features

✅ **Working Contact Form**
- HTMX-powered for smooth user experience
- Form validation and error handling
- Loading states and user feedback
- Email sending capability

✅ **Email Service**
- Async email sending with aiosmtplib
- HTML and plain text email formats
- Professional email templates
- Development mode (logs emails to console)

## Setup for Production

To enable email sending in production, create a `.env` file with your email settings:

```bash
# Copy the example file
cp .env.example .env
```

Then edit `.env` and configure your email settings:

```env
# Email settings (for contact form)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
TO_EMAIL=brian.hardin@icloud.com
```

### Gmail Setup

1. Enable 2-factor authentication on your Gmail account
2. Generate an "App Password" in your Google Account settings
3. Use the app password (not your regular password) in `SMTP_PASSWORD`

### Other Email Providers

The service supports any SMTP provider. Just update the SMTP settings accordingly:

- **Outlook/Hotmail**: `smtp-mail.outlook.com:587`
- **Yahoo**: `smtp.mail.yahoo.com:587`
- **Custom SMTP**: Use your provider's settings

## Development Mode

When no email credentials are provided, the contact form works in development mode:
- Forms still submit successfully
- Email content is logged to the console
- Users see success messages
- No actual emails are sent

## Security

- Email addresses are validated using Pydantic
- All form inputs are sanitized
- HTML content is escaped in email templates
- No sensitive data is logged

## Testing

The contact form includes comprehensive tests:
- Form submission with valid data
- Validation error handling
- Missing field validation
- Success/error message display

Run tests with: `uv run pytest tests/ -v`
