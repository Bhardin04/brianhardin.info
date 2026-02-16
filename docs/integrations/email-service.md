# Email Service Configuration

Complete guide for configuring email functionality in the contact form.

## Overview

The brianhardin.info website includes a contact form with email sending capabilities using `aiosmtplib` for async email delivery. The service supports both development and production modes.

## Development Mode

By default, the contact form operates in development mode when no email credentials are configured:

- ✅ Forms submit successfully
- ✅ Email content is logged to console
- ✅ Users see success messages
- ✅ No actual emails are sent

This allows full development and testing without email setup.

## Production Email Setup

### 1. Environment Configuration

Create a `.env` file with your email settings:

```bash
# Copy the example file
cp .env.example .env
```

Configure your email provider settings:

```env
# Email settings (for contact form)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
TO_EMAIL=brian.hardin@icloud.com
```

### 2. Provider-Specific Setup

#### Gmail Setup

1. **Enable 2-Factor Authentication**
   - Go to your Google Account settings
   - Enable 2-factor authentication if not already enabled

2. **Generate App Password**
   - Visit [Google Account App Passwords](https://myaccount.google.com/apppasswords)
   - Generate a new app password for "Mail"
   - Use this password (not your regular password) in `SMTP_PASSWORD`

3. **Gmail Configuration**
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-16-character-app-password
   FROM_EMAIL=your-email@gmail.com
   TO_EMAIL=destination@example.com
   ```

#### Other Email Providers

**Outlook/Hotmail:**
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
```

**Yahoo Mail:**
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your-email@yahoo.com
SMTP_PASSWORD=your-app-password
```

**Custom SMTP Provider:**
```env
SMTP_SERVER=your-smtp-server.com
SMTP_PORT=587  # or 465 for SSL
SMTP_USERNAME=your-username
SMTP_PASSWORD=your-password
```

## Email Templates

The service sends both HTML and plain text versions of emails:

### HTML Template
- Professional formatting
- Sender information clearly displayed
- Message content with proper formatting
- Responsive design for mobile email clients

### Plain Text Template
- Fallback for clients that don't support HTML
- Clean, readable format
- All essential information included

## Security Features

### Input Validation
- **Email Validation**: Uses Pydantic for robust email address validation
- **Input Sanitization**: All form inputs are sanitized before processing
- **HTML Escaping**: HTML content is escaped in email templates

### Data Protection
- **No Logging**: Sensitive data like email content is never logged
- **Memory Cleanup**: Email content is cleared from memory after sending
- **Secure Headers**: Proper email headers for authentication

## Testing Email Configuration

### 1. Test in Development
```bash
# Start the server
uv run fastapi dev app/main.py --port 8000

# Submit the contact form at http://127.0.0.1:8000/contact
# Check console output for email content
```

### 2. Test in Production
```bash
# Set environment variables
export SMTP_SERVER=smtp.gmail.com
export SMTP_USERNAME=your-email@gmail.com
# ... other variables

# Start server and test form submission
```

### 3. Automated Testing
```bash
# Run contact form tests
uv run pytest tests/test_main.py::test_contact_form -v
```

## Troubleshooting

### Common Issues

**Authentication Failed:**
- Verify app password is correct (not regular password)
- Ensure 2-factor authentication is enabled
- Check username/email format

**Connection Timeout:**
- Verify SMTP server and port
- Check firewall/network restrictions
- Try different port (587 vs 465)

**Permission Denied:**
- Enable "Less secure app access" if required
- Use app-specific passwords instead of account passwords
- Check provider-specific security settings

**Emails Not Received:**
- Check spam/junk folders
- Verify TO_EMAIL address is correct
- Test with different email providers

### Debug Mode

Enable debug logging to troubleshoot email issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Considerations

### Async Email Sending
- Emails are sent asynchronously to prevent blocking
- Form responses are immediate even if email sending takes time
- Background task handles email delivery

### Rate Limiting
Consider implementing rate limiting for production:
- Limit form submissions per IP
- Implement CAPTCHA for additional protection
- Monitor for abuse patterns

## Production Recommendations

1. **Use Dedicated Email Service**
   - Consider services like SendGrid, Mailgun, or AWS SES
   - Better deliverability and monitoring
   - Professional email infrastructure

2. **Monitor Email Delivery**
   - Track delivery success/failure rates
   - Log email sending attempts (without content)
   - Set up alerts for delivery failures

3. **Backup Contact Methods**
   - Provide alternative contact information
   - Include social media links
   - Consider adding phone number

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SMTP_SERVER` | Yes | SMTP server hostname | `smtp.gmail.com` |
| `SMTP_PORT` | Yes | SMTP server port | `587` |
| `SMTP_USERNAME` | Yes | SMTP authentication username | `user@gmail.com` |
| `SMTP_PASSWORD` | Yes | SMTP authentication password | `app-password` |
| `FROM_EMAIL` | Yes | Email address for outgoing messages | `user@gmail.com` |
| `TO_EMAIL` | Yes | Destination email address | `contact@example.com` |

All variables must be set for production email sending. If any are missing, the service falls back to development mode.
