# brianhardin.info
> Personal Brand Website built with FastAPI, HTMX, and Tailwind CSS

A modern, responsive personal website showcasing professional experience, projects, and providing an interactive contact form with a comprehensive design system.

## 🚀 Quick Start

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

## ✨ Features

### 🎨 Professional Design System
- ✅ **150+ Design Tokens** - Comprehensive CSS custom properties for colors, spacing, typography
- ✅ **Python-Inspired Color Palette** - Professional blue and gold color scheme
- ✅ **Responsive Typography** - Inter font with responsive scaling across devices
- ✅ **Dark Mode Support** - Complete dark/light theme system with localStorage persistence
- ✅ **Professional Animations** - Subtle hover effects, loading states, and micro-interactions

### 🧩 Reusable Components
- ✅ **Enhanced Cards** - Professional project cards, feature cards, stats cards
- ✅ **Form Components** - Professional contact form with validation and loading states
- ✅ **Badge System** - Status indicators, skill badges, and content tags
- ✅ **Progress Bars** - Animated skill progress indicators
- ✅ **Interactive Elements** - Tooltips, toasts, skeleton loading states

### 📱 Modern User Experience
- ✅ **Mobile-First Design** - Responsive layout optimized for all screen sizes
- ✅ **Hero Sections** - Consistent, professional landing sections across all pages
- ✅ **Interactive Contact Form** - HTMX-powered with email integration
- ✅ **Project Portfolio** - Enhanced showcase with high-quality project screenshots
- ✅ **Professional Resume** - Complete resume page with brand-consistent design
- ✅ **Blog System** - Professional blog layout with tagging and filtering
- ✅ **Performance Optimized** - Fast loading with optimized CSS, animations, and SVG compression

### 🎮 Interactive Project Demos
- ✅ **Payment Processing Demo** - Automated payment application workflow
- ✅ **Data Pipeline Demo** - NetSuite to SAP data integration showcase
- ✅ **Sales Dashboard Demo** - Revenue analytics with interactive charts
- ✅ **Collections Dashboard Demo** - DSO tracking and collector performance
- ✅ **WebSocket Real-time Updates** - Live data streaming for demos
- ✅ **Demo Analytics** - Performance monitoring and user interaction tracking

### 🛠 Technical Features
- ✅ **FastAPI Backend** - Modern Python web framework
- ✅ **HTMX Integration** - Dynamic interactions without JavaScript frameworks
- ✅ **WebSocket Support** - Real-time data updates for interactive demos
- ✅ **Email Service** - Async email sending with production/dev modes
- ✅ **SEO Optimized** - Meta tags, structured data, and canonical URLs
- ✅ **Testing Suite** - Pytest + Puppeteer for E2E testing
- ✅ **CI/CD Pipeline** - GitHub Actions with linting, testing, and deployment
- ✅ **Branch Protection** - PR-required workflow with CI checks on main

## 🎨 Design System

### Color Palette
- **Primary**: Python-inspired blues (#3b82f6 to #1e3a8a)
- **Secondary**: Gold accents (#eab308 to #713f12)
- **Semantic**: Success, warning, and error states
- **Neutrals**: Comprehensive gray scale with dark mode variants

### Typography
- **Font Family**: Inter (sans-serif), Fira Code (monospace)
- **Responsive Scales**: Mobile-first with desktop enhancements
- **Font Weights**: Light (300) to Extra Bold (800)

### Components
- **Buttons**: Primary, secondary with hover animations
- **Cards**: Shadow effects, border variations, interactive states
- **Forms**: Enhanced inputs with icons and validation
- **Badges**: Status indicators, skill tags, content categories

## 🏗 Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: HTMX + Custom CSS Design System
- **Styling**: CSS Custom Properties + Tailwind CSS
- **Email**: aiosmtplib for async email sending
- **Testing**: Pytest + Puppeteer for E2E testing
- **Deployment**: Docker + Docker Compose ready

## 📁 Project Structure

```
brianhardin.info/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── models/              # Pydantic models
│   │   ├── contact.py       # Contact form validation
│   │   ├── project.py       # Project & case study models
│   │   ├── demo.py          # Interactive demo models
│   │   └── blog.py          # Blog post models
│   ├── routers/             # API routes
│   │   ├── pages.py         # Main page routes
│   │   ├── projects.py      # Project portfolio & detail routes
│   │   ├── demos.py         # Demo API & WebSocket endpoints
│   │   ├── api.py           # Contact form & utility APIs
│   │   └── blog.py          # Blog routes
│   ├── services/            # Business logic
│   │   ├── email.py         # Async email with XSS protection
│   │   ├── project.py       # Centralized project data service
│   │   ├── demo.py          # Demo data & processing services
│   │   ├── websocket.py     # WebSocket connection management
│   │   └── blog.py          # Blog service
│   ├── static/
│   │   ├── css/styles.css   # Design system (2,500+ lines)
│   │   ├── js/              # Client-side JavaScript
│   │   │   ├── chart-utils.js
│   │   │   ├── connection-manager.js
│   │   │   ├── error-handler.js
│   │   │   ├── analytics-*.js
│   │   │   ├── websocket-client.js
│   │   │   └── user-preferences.js
│   │   └── images/          # SVG brand assets & project images
│   └── templates/           # Jinja2 templates
│       ├── base.html        # Base template with responsive nav
│       ├── index.html       # Homepage with hero section
│       ├── projects.html    # Project showcase with filtering
│       ├── project_detail.html  # Case study detail pages
│       ├── demos/           # Interactive demo templates
│       │   ├── index.html
│       │   ├── sales_dashboard.html
│       │   ├── collections_dashboard.html
│       │   ├── payment_processing.html
│       │   └── data_pipeline.html
│       ├── blog/            # Blog system templates
│       ├── resume.html      # Professional resume page
│       ├── about.html       # About page
│       └── contact.html     # Contact form
├── docs/                    # Documentation
├── tests/                   # Pytest test suite
├── testing/                 # E2E testing with Puppeteer
└── .github/workflows/       # CI/CD pipeline
```

## 🎯 Documentation

### Setup & Configuration
- [Installation Guide](docs/setup/installation.md) - Complete project setup
- [Development Setup](docs/setup/development.md) - Local development environment

### Architecture
- [Project Structure](docs/architecture/project-structure.md) - Directory organization
- [Design System](docs/features/design-system.md) - CSS architecture and components

### Features
- [Contact Form](docs/features/contact-form.md) - Setup and configuration
- [Responsive Design](docs/features/responsive-design.md) - UI/UX considerations
- [Interactive Demos](docs/features/interactive-demos.md) - Hands-on project experiences

### Development
- [Testing Guide](docs/development/testing.md) - Testing strategy and execution
- [Contributing](docs/development/contributing.md) - How to contribute
- [Deployment](docs/development/deployment.md) - Production deployment guide
- [Roadmap](docs/development/roadmap.md) - Planned improvements

### Integrations
- [MCP Setup](docs/integrations/mcp-setup.md) - Model Context Protocol configuration
- [Email Service](docs/integrations/email-service.md) - Email configuration options

### Troubleshooting
- [Template Debugging](TEMPLATE_DEBUGGING.md) - Project detail template issues and solutions

## 📊 Development Status

### ✅ Completed Features
- **Design System**: Professional CSS architecture with 150+ design tokens
- **Component Library**: Reusable components (cards, buttons, forms, badges)
- **Responsive Design**: Mobile-first with desktop enhancements
- **Contact Form**: Production-ready with comprehensive testing
- **Dark Mode**: Complete light/dark theme system
- **Page Templates**: All pages updated with consistent design
- **Performance**: Optimized CSS and loading states with SVG compression (4.3KB saved)
- **SEO**: Meta tags, structured data, canonical URLs
- **Project Portfolio**: High-quality project screenshots and enhanced showcase
- **Hero Sections**: Compelling CTAs and engaging project descriptions
- **Image Optimization**: Comprehensive SVG optimization for better performance
- **Professional Resume**: Complete resume page with brand integration and navigation

### 🔄 Current Focus
- **Content Enhancement**: Adding more projects and blog content
- **Performance Optimization**: Analytics and performance tracking refinements

### 🚀 Upcoming Features
- **Blog CMS**: Admin interface for content management
- **Portfolio Expansion**: Additional project showcases
- **Custom 404 Pages**: Branded error pages
- **Sitemap Generation**: XML sitemap for search engines

## 🛠 Quick Commands

```bash
# Development
uv run fastapi dev app/main.py --port 8000

# Testing
uv run pytest tests/ -v

# E2E Testing
cd testing && npm test

# Docker
docker-compose up --build

# Dependencies
uv sync

# Code Quality
uv run ruff check
uv run mypy app/
```

## 🎨 Design System Usage

### CSS Custom Properties
```css
/* Colors */
var(--color-primary-500)    /* Main brand color */
var(--color-secondary-500)  /* Accent color */
var(--color-success-500)    /* Success states */

/* Typography */
var(--font-sans)            /* Inter font family */
var(--text-responsive-3xl)  /* Responsive heading */
var(--leading-relaxed)      /* Line height */

/* Spacing */
var(--space-4)              /* 1rem spacing */
var(--space-8)              /* 2rem spacing */

/* Components */
.btn-primary                /* Primary button */
.card                       /* Basic card */
.badge-success              /* Success badge */
```

### Component Classes
```html
<!-- Buttons -->
<button class="btn-primary">Primary Action</button>
<button class="btn-secondary">Secondary Action</button>

<!-- Cards -->
<div class="card p-6 hover:shadow-xl">Card Content</div>

<!-- Badges -->
<span class="badge badge-primary">Status</span>

<!-- Progress Bars -->
<div class="progress-bar">
  <div class="progress-fill" style="width: 75%"></div>
</div>
```

## 📄 License

Personal project - All rights reserved

---

**Author**: Brian Hardin
**Contact**: Available through the website contact form
**Portfolio**: https://brianhardin.info

Built with ❤️ using FastAPI, HTMX, and a custom CSS design system
