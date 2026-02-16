# Project Structure

Overview of the brianhardin.info project directory organization and architecture.

## Root Directory Structure

```
brianhardin.info/
├── app/                    # Main application code
│   ├── __init__.py
│   ├── main.py            # FastAPI application entry point
│   ├── config.py          # Configuration settings
│   ├── models/            # Pydantic models
│   ├── routers/           # API route handlers
│   ├── services/          # Business logic services
│   ├── static/            # Static assets (CSS, JS, images)
│   └── templates/         # Jinja2 HTML templates
├── docs/                   # Project documentation
│   ├── setup/             # Setup and installation guides
│   ├── architecture/      # System architecture docs
│   ├── features/          # Feature-specific documentation
│   ├── development/       # Development and contribution guides
│   └── integrations/      # Third-party integrations
├── testing/               # Test artifacts and guides
│   ├── reports/           # Test reports
│   ├── guides/            # Testing guides
│   └── screenshots/       # Visual test artifacts
├── tests/                 # Python test suite
├── docker-compose.yml     # Docker composition
├── Dockerfile             # Container definition
├── pyproject.toml         # Python project configuration
├── uv.lock               # Dependency lock file
└── README.md             # Project overview
```

## Application Structure (`app/`)

### Core Files

- **`main.py`** - FastAPI application factory and main entry point
- **`config.py`** - Application configuration and environment variables

### Models (`app/models/`)

Pydantic models for data validation and serialization:

- **`contact.py`** - Contact form data model with field validation
- **`project.py`** - Project and case study models (categories, metrics, timelines)
- **`demo.py`** - Interactive demo models (sessions, payments, invoices, KPIs)
- **`blog.py`** - Blog post models

### Routers (`app/routers/`)

FastAPI route handlers organized by functionality:

- **`pages.py`** - Main website pages (home, about, contact, etc.)
- **`projects.py`** - Project portfolio and case study detail routes
- **`demos.py`** - Interactive demo page routes, API endpoints, and WebSocket handler
- **`api.py`** - Contact form, analytics, error reporting, health check endpoints
- **`blog.py`** - Blog listing and post detail routes

### Services (`app/services/`)

Business logic and external service integrations:

- **`email.py`** - Email sending service with async support and XSS protection
- **`demo.py`** - Demo business logic (payment processing, data pipeline, dashboard, collections services)
- **`websocket.py`** - WebSocket connection management, real-time data simulation
- **`blog.py`** - Blog post retrieval, filtering, and search

### Static Assets (`app/static/`)

Frontend assets served directly:

```
static/
├── css/
│   └── styles.css             # Design system (2,500+ lines)
├── js/
│   ├── chart-utils.js         # Chart drill-down, zoom, export
│   ├── connection-manager.js  # Offline/online detection, fetch retry
│   ├── error-handler.js       # Global error handling & recovery
│   ├── error-boundary.js      # Component error boundaries
│   ├── analytics-dashboard.js # Analytics overlay UI
│   ├── analytics-tracker.js   # User interaction tracking
│   ├── performance-monitor.js # FPS, memory, network monitoring
│   ├── websocket-client.js    # WebSocket client with reconnection
│   ├── user-preferences.js    # localStorage preferences manager
│   └── preferences-ui.js      # Preferences modal UI
├── images/
│   ├── brand/                 # SVG brand assets (logo, favicon, pattern)
│   ├── projects/              # Project SVG illustrations
│   └── headshot.png           # Profile photo
└── favicon.ico                # Site favicon
```

### Templates (`app/templates/`)

Jinja2 HTML templates:

- **`base.html`** - Base template with responsive nav, mobile hamburger menu, dark mode
- **`index.html`** - Homepage template
- **`about.html`** - About page template
- **`contact.html`** - Contact page with form
- **`resume.html`** - Resume/CV display
- **`projects.html`** - Project portfolio with category filtering
- **`project_detail.html`** - Case study detail pages
- **`demos/`** - Interactive demo templates
  - **`index.html`** - Demo portal landing page
  - **`payment_processing.html`** - Payment application demo
  - **`data_pipeline.html`** - Data integration demo
  - **`sales_dashboard.html`** - Sales analytics demo
  - **`collections_dashboard.html`** - Collections management demo
  - **`automation_suite.html`** - Automation placeholder

## Documentation Structure (`docs/`)

Organized documentation following best practices:

### Setup (`docs/setup/`)
- Installation and initial setup guides
- Configuration documentation
- Development environment setup

### Architecture (`docs/architecture/`)
- System overview and design decisions
- Project structure explanation
- API reference documentation

### Features (`docs/features/`)
- Feature-specific documentation
- Contact form setup and configuration
- Responsive design considerations

### Development (`docs/development/`)
- Testing strategies and guides
- Contributing guidelines
- Deployment instructions
- Project roadmap

### Integrations (`docs/integrations/`)
- Third-party service configurations
- MCP server setup
- Email service configuration

## Configuration Files

### Python Configuration

- **`pyproject.toml`** - Python project metadata, dependencies, and tool configuration
- **`uv.lock`** - Exact dependency versions for reproducible builds

### Docker Configuration

- **`Dockerfile`** - Container image definition
- **`docker-compose.yml`** - Multi-container development setup

### Environment Configuration

- **`.env.example`** - Template for environment variables
- **`.env`** - Local environment configuration (not in version control)

## Design Principles

### Separation of Concerns
- **Models**: Data validation and serialization
- **Routers**: HTTP request/response handling
- **Services**: Business logic and external integrations
- **Templates**: Presentation layer

### Modular Architecture
- Feature-based organization
- Clear dependency boundaries
- Easy to test and maintain

### Documentation-First
- Comprehensive documentation structure
- Examples and guides for all features
- Clear setup and contribution paths

## Development Workflow

1. **Models** - Define data structures
2. **Services** - Implement business logic
3. **Routers** - Create API endpoints
4. **Templates** - Build user interface
5. **Tests** - Ensure quality and reliability

This structure supports scalable development while maintaining clarity and ease of navigation for both new and experienced developers.
