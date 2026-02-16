# Installation Guide

Complete setup guide for the brianhardin.info personal website project.

## Prerequisites

- **Python 3.12+** - Modern Python version
- **uv** - Fast Python package manager
- **Git** - Version control
- **Node.js 18+** - For testing tools (optional)

## Installation Steps

### 1. Clone Repository
```bash
git clone <repository-url>
cd brianhardin.info
```

### 2. Install Dependencies
```bash
# Install Python dependencies with uv
uv sync

# Activate virtual environment (optional)
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

### 3. Environment Configuration
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings (optional for development)
nano .env
```

### 4. Verify Installation
```bash
# Run the development server
uv run fastapi dev app/main.py --port 8000

# Visit http://127.0.0.1:8000 to see the website
```

## Quick Start Commands

```bash
# Start development server
uv run fastapi dev app/main.py --port 8000

# Run tests
uv run pytest tests/ -v

# Run with Docker (alternative)
docker-compose up --build
```

## Development Setup

For development work, see [Development Setup](development.md) for additional configuration options.

## Email Configuration

The contact form works in development mode without email configuration. For production email sending, see [Email Service Configuration](../integrations/email-service.md).

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure dependencies are installed
uv sync
```

**Port Already in Use:**
```bash
# Use a different port
uv run fastapi dev app/main.py --port 8001
```

**Permission Errors:**
```bash
# Check directory permissions
ls -la
```

## Next Steps

- [Configure Email Service](../integrations/email-service.md)
- [Set up Development Environment](development.md)
- [Understand Project Architecture](../architecture/overview.md)
