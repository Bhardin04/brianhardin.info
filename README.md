# brianhardin.info
> Personal Brand Website built with FastAPI, HTMX, and Tailwind CSS

A modern, responsive personal website showcasing professional experience, projects, and providing an interactive contact form.

## Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd brianhardin.info
   uv sync
   ```

2. **Run Development Server**
   ```bash
   uv run fastapi dev app/main.py --port 8000
   ```

3. **Visit Website**
   Open http://127.0.0.1:8000 in your browser

## Features

- ✅ **Modern Responsive Design** - Mobile-first approach with Tailwind CSS
- ✅ **Interactive Contact Form** - HTMX-powered with email integration
- ✅ **Project Portfolio** - Showcase of professional work
- ✅ **Professional Resume** - Comprehensive experience display
- ✅ **Email Service** - Async email sending with production/dev modes

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTMX + Tailwind CSS
- **Email**: aiosmtplib for async email sending
- **Testing**: Pytest + Puppeteer for E2E testing
- **Deployment**: Docker + Docker Compose ready

## Documentation

### Setup & Configuration
- [Installation Guide](docs/setup/installation.md) - Complete project setup
- [Configuration](docs/setup/configuration.md) - Environment variables and settings
- [Development Setup](docs/setup/development.md) - Local development environment

### Architecture
- [System Overview](docs/architecture/overview.md) - High-level architecture
- [Project Structure](docs/architecture/project-structure.md) - Directory organization
- [API Reference](docs/architecture/api-reference.md) - Endpoint documentation

### Features
- [Contact Form](docs/features/contact-form.md) - Setup and configuration
- [Responsive Design](docs/features/responsive-design.md) - UI/UX considerations

### Development
- [Testing Guide](docs/development/testing.md) - Testing strategy and execution
- [Contributing](docs/development/contributing.md) - How to contribute
- [Deployment](docs/development/deployment.md) - Production deployment guide
- [Roadmap](docs/development/roadmap.md) - Planned improvements

### Integrations
- [MCP Setup](docs/integrations/mcp-setup.md) - Model Context Protocol configuration
- [Email Service](docs/integrations/email-service.md) - Email configuration options

## Development Status

- **Contact Form**: ✅ Production ready with comprehensive testing
- **Responsive Design**: ⚠️ Needs mobile optimization (see [roadmap](docs/development/roadmap.md))
- **Content**: ⚠️ Projects section needs more content
- **Testing**: ✅ Comprehensive test suite with Puppeteer

## Quick Commands

```bash
# Run tests
uv run pytest tests/ -v

# Start development server
uv run fastapi dev app/main.py --port 8000

# Run with Docker
docker-compose up --build

# Install dependencies
uv sync
```

## License

Personal project - All rights reserved

---

**Author**: Brian Hardin  
**Contact**: Available through the website contact form