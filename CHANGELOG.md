# Changelog

All notable changes to the brianhardin.info project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Admin Panel / CMS** - Full content management system with GitHub OAuth authentication
  - Blog CRUD: create, edit, delete, publish/unpublish with markdown rendering
  - Project CRUD: full management including case study data (problem/solution/outcome/timeline)
  - Contact inbox: view, mark read, archive, and delete contact form submissions
  - Site settings: key-value configuration management
  - Dashboard: stats cards with post/project/message counts
  - Standalone admin layout with sidebar navigation and dark mode
- **Database Layer** - SQLAlchemy 2.0 async ORM with PostgreSQL (production) and SQLite (local dev)
  - 5 tables: blog_posts, projects, contact_messages, admin_sessions, site_settings
  - Async engine with `expire_on_commit=False` for safe post-commit access
  - Feature-flagged migration: `USE_DATABASE` env var controls DB vs in-memory routing
- **GitHub OAuth** - Admin authentication via GitHub OAuth with session-based access
  - Configurable admin username via `ADMIN_GITHUB_USERNAME`
  - 24-hour session TTL with `secrets.token_urlsafe(48)` tokens
  - HTTPS proxy header support for Render deployment
- **Data Seeding** - `python -m app.scripts.seed` migrates hardcoded data to database (idempotent)
- **DB Adapters** - SQLAlchemy to Pydantic model converters for public routes
- **Contact Form DB Storage** - Contact submissions saved to database alongside email sending
- **Rate Limiting** - Per-route rate limits using `slowapi` on contact form (1/min, 3/hr), analytics (30/min), error reporting (10/min), demo sessions (10/min), and demo data endpoints (20/min)
- **CSRF Protection** - Double Submit Cookie pattern on contact form with HMAC-signed tokens, 1-hour expiry, and `httponly`/`samesite=strict` cookie
- **Security Tests** - Comprehensive test suite for CSRF token generation/validation, protection flow, and rate limiting behavior
- **Breadcrumb Navigation** - Consistent breadcrumb nav on project detail and all demo pages
- **Custom Error Pages** - Styled 404 and 500 error pages extending base template
- **XML Sitemap** - `/sitemap.xml` endpoint with dynamic project/blog URLs from database
- **RSS Feed** - `/blog/feed.xml` endpoint with RSS 2.0 format
- **Demo Test Suite** - 38 tests covering demo page rendering, API endpoints, service business logic, session management, and WebSocket communication
- **Database Tests** - 23 tests covering DB services, adapters, seed script, and JSON roundtrips
- **ProjectService** - Centralized project data service as single source of truth

### Changed
- **`USE_DATABASE` default** - Changed from `false` to `true`; database is now the primary content source
- **Pre-commit Hooks** - Removed redundant `black` and `isort` (handled by ruff); updated ruff to v0.12.2, pre-commit-hooks to v5.0.0, mypy to v1.14.1, bandit to 1.8.3
- **Pydantic V2 Migration** - Replaced deprecated `class Config` with `model_config = ConfigDict()` and `.dict()` with `.model_dump()` across all models and services
- **Starlette TemplateResponse** - Updated all `TemplateResponse` calls to new API signature

### Security
- **GitHub OAuth Admin Access** - Only configured GitHub username can access admin panel
- **SMTP Header Injection Prevention** - Sanitize email subject by stripping `\r` and `\n` characters
- **Demo Session Limits** - `MAX_SESSIONS=100` and `SESSION_TTL_SECONDS=3600` to prevent unbounded memory growth
- **WebSocket Connection Limits** - `MAX_CONNECTIONS=200` and `MAX_CONNECTIONS_PER_SESSION=5`
- **Pipeline Record Cap** - Capped WebSocket pipeline `total_records` to 1000

### Fixed
- **500 Error Handler Type** - Changed exception parameter from `StarletteHTTPException` to `Exception`
- **OAuth Redirect URI** - Added `--proxy-headers` and `--forwarded-allow-ips *` to Dockerfile for HTTPS behind Render's proxy
- **Naive Datetime Handling** - Normalized to naive UTC (`datetime.now(UTC).replace(tzinfo=None)`) for cross-database compatibility
- **Dark mode blog sidebar** - Added missing `dark:bg-gray-800` to "About This Blog" card
- **Footer whitespace** - Added sticky footer layout, reduced excessive padding
- **Brand alignment** - Replaced all undefined `primary-*`/`secondary-*` Tailwind classes with `brand-*` across all public templates
- **Dark mode h1 titles** - Fixed `.text-gradient-primary` using wrong gray token in dark mode (was invisible dark text on dark bg)
- **Missing card accent CSS** - Added `card-accent-blue/emerald/purple/orange` definitions (used in resume and homepage but had no CSS)
- **Demos page brand alignment** - Replaced off-brand `slate-*`/`blue-*` hero gradient, CTA buttons, and card backgrounds
- **Font-size override** - Narrowed global `font-size: 16px` rule from `body, p, div, span, a, button` to `input, textarea, select` only
- **Link specificity** - Scoped `a:visited` color with `:not()` selectors to prevent overriding button/nav link classes

## [1.4.0] - 2026-02-15

### Added
- ✅ **Interactive Demo Backend** - FastAPI router, services, and Pydantic models for demo API endpoints
- ✅ **WebSocket Support** - Real-time data streaming with connection management and demo simulation
- ✅ **Demo Templates** - Payment processing, data pipeline, sales dashboard, collections dashboard, and demo index page
- ✅ **Client-side JavaScript** - Analytics dashboard, analytics tracker, performance monitor, user preferences, preferences UI, WebSocket client
- ✅ **Project Case Studies** - Expanded project model with problem/solution/outcome framework, metrics, timelines
- ✅ **Project Detail Pages** - Full case study layout with hero, sidebar, metrics grid, and CTA sections
- ✅ **Project Portfolio Filtering** - Category filtering, featured badges, and interactive demo buttons
- ✅ **CSS Design System** - Comprehensive 2,500+ line design system with tokens, components, and dark mode
- ✅ **Brand Assets** - SVG favicon, logo, pattern, and Python icon
- ✅ **Service Worker Stub** - PWA-ready service worker endpoint
- ✅ **Branch Protection** - PR-required workflow with CI status checks on main

### Fixed
- ✅ **Connection Manager Bug** - Fixed infinite recursion in fetch retry logic
- ✅ **Sales Dashboard JS Errors** - Fixed runtime errors from missing `advancedChartManager`
- ✅ **Mobile Navigation** - Restored hamburger menu for responsive design
- ✅ **Skip-to-Content Link** - Restored accessibility skip navigation
- ✅ **Ruff Lint Errors** - Fixed all 20 linting issues (trailing whitespace, deprecated typing imports, unused imports)
- ✅ **Test Failures** - Updated tests to match new templates and project data

### Security
- ✅ **Cryptographic SECRET_KEY** - Replaced hardcoded key with `secrets.token_urlsafe(32)`
- ✅ **Input Validation** - Added field length limits on contact form with Pydantic validators
- ✅ **XSS Prevention** - Added `html.escape()` to email service HTML generation
- ✅ **Error Info Hiding** - Removed raw error details from user-facing API responses
- ✅ **Logging Improvements** - Replaced print statements with structured logging, truncated sensitive data

### Changed
- ✅ **Base Template** - Enhanced SEO structured data, PWA meta tags, brand logo in nav, system dark mode detection
- ✅ **Navigation** - Added Demos and Resume links, sticky nav with backdrop blur
- ✅ **Footer** - Redesigned with SVG social icons and brand pattern
- ✅ **Removed Backup Files** - Cleaned up .svg.backup and .html.backup files, added `*.backup` to .gitignore

### Documentation
- ✅ **README** - Updated project structure, features list, and development status
- ✅ **CHANGELOG** - Comprehensive v1.4.0 release notes
- ✅ **Roadmap** - Updated completed items and current priorities
- ✅ **Development Docs** - Added navigation investigation, phase 1 report, and performance fixes docs

## [1.3.0] - 2025-01-10 (Phase 1 Complete)

### 🔒 Security (Critical Fixes)
- ✅ **Fixed XSS vulnerabilities** - Added proper HTML escaping in email service using `html.escape()`
- ✅ **Replaced weak SECRET_KEY** - Now uses cryptographically secure random generation with `secrets.token_urlsafe(32)`
- ✅ **Fixed information disclosure** - Removed error details from user-facing messages, added proper logging
- ✅ **Added input validation** - Implemented field length limits (name: 100, subject: 200, message: 5000 chars)
- ✅ **Added security headers** - X-Frame-Options, CSP, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy
- ✅ **Improved logging** - Structured logging with sensitive data protection and proper error tracking

### 📱 Responsive Design
- ✅ **Fixed horizontal overflow** - Enhanced global CSS with better box-sizing and container handling
- ✅ **Touch targets verified** - Confirmed 44px minimum already implemented for accessibility
- ✅ **Form inputs verified** - Confirmed 44px minimum height already implemented

### 🔍 SEO Enhancements
- ✅ **Enhanced meta tags** - Added language, geo, performance optimization tags
- ✅ **Improved structured data** - Comprehensive Person/ProfessionalService schema with skills and services
- ✅ **Added website schema** - SearchAction capability and publisher information
- ✅ **Performance optimizations** - Preconnect to external domains (fonts.googleapis.com, cdn.tailwindcss.com)

### 🛠 Template Fixes
- ✅ **Fixed project detail template** - Created robust template handling both simple and complex project data
- ✅ **Added comprehensive error handling** - Safe template rendering with all nested attributes (problem/solution/outcome)
- ✅ **Enhanced project showcase** - Problem-Solution-Outcome sections, metrics, timelines, achievements
- ✅ **Fixed category/status rendering** - Template now handles both enum and string values properly

### 🧪 Testing & Quality
- ✅ **All tests passing** - Fixed template rendering issues and validation errors
- ✅ **Security testing** - Verified XSS protection and input validation limits
- ✅ **Header testing** - Confirmed all security headers are properly set
- ✅ **Contact form testing** - Validated new field length restrictions work correctly

### 🔧 Development Infrastructure
- ✅ **CORS configuration** - Restrictive CORS settings for production security
- ✅ **Middleware architecture** - Custom security headers middleware implementation
- ✅ **Error handling** - Improved error logging without information disclosure
- ✅ **Input sanitization** - Comprehensive validation on all user inputs

### Changed
- Extract common project data into shared service class
- Replace all `print()` statements with proper logging framework
- Move hardcoded sample data to separate data files
- Separate development and production email service logic
- Move all hardcoded values to environment variables

### Performance
- Optimize related posts algorithm (improve O(n²) complexity)
- Implement Redis caching for frequently accessed data
- Use UUID instead of hash-based ID generation

### Documentation
- Add comprehensive code review improvements list
- Create change log for tracking project improvements

## [1.2.0] - 2025-01-09

### Added
- ✅ **Professional Resume Page** - Complete resume template with brand-consistent design
- ✅ **Resume Navigation Integration** - Added resume link to main navigation and CTAs
- ✅ **Cross-Page Resume CTAs** - Added resume buttons to home and about pages
- ✅ **Resume SEO Optimization** - Comprehensive meta tags and structured data
- ✅ **Professional Progress Bars** - Branded skill visualization with gradient fills
- ✅ **Resume Contact Integration** - Seamless connection to contact form

### Changed
- ✅ **Navigation Structure** - Added resume link between Projects and Blog
- ✅ **Home Page CTAs** - Enhanced hero section with resume access
- ✅ **About Page Sidebar** - Added resume viewing option for easy access

### Documentation
- ✅ **README Updates** - Documented resume integration and navigation changes
- ✅ **Project Structure** - Updated documentation to include resume.html

## [1.1.0] - 2025-01-09

### Added
- ✅ **High-Quality Project Screenshots** - Replaced SVG placeholders with professional project images
- ✅ **Comprehensive Case Study Data** - Added detailed problem-solution-outcome framework for all projects
- ✅ **Enhanced Project Narratives** - Compelling user stories and business impact metrics
- ✅ **Technical Architecture Details** - Implementation insights and lessons learned
- ✅ **Project Timeline Information** - Development process and milestone tracking
- ✅ **Engaging Hero Sections** - Compelling CTAs and project descriptions
- ✅ **Template Debugging Documentation** - Comprehensive troubleshooting guide for project detail issues

### Performance
- ✅ **SVG Optimization** - Compressed all project images, saving 4,310 bytes total
- ✅ **Image Performance** - Optimized analytics-dashboard.svg, automation-suite.svg, chat-api.svg, ecommerce-api.svg, portfolio-website.svg

### Fixed
- ✅ **Project Detail Template** - Resolved 500 Internal Server Error when clicking "View Details"
- ✅ **Template Safety** - Added comprehensive safety checks for nested project attributes
- ✅ **Fallback Implementation** - Simplified template ensures stable user experience

### Changed
- ✅ **Project Data Structure** - Enhanced models with comprehensive case study information
- ✅ **Content Quality** - Improved project descriptions with quantifiable metrics
- ✅ **Visual Hierarchy** - Better content organization and readability

### Documentation
- ✅ **Template Debugging Guide** - Created TEMPLATE_DEBUGGING.md for future development
- ✅ **README Updates** - Documented all recent improvements and current status
- ✅ **Changelog Updates** - Comprehensive tracking of project evolution

## [1.0.0] - 2025-01-08

### Added
- ✅ **150+ Design Tokens** - Comprehensive CSS custom properties for colors, spacing, typography
- ✅ **Python-Inspired Color Palette** - Professional blue and gold color scheme
- ✅ **Responsive Typography** - Inter font with responsive scaling across devices
- ✅ **Dark Mode Support** - Complete dark/light theme system with localStorage persistence
- ✅ **Professional Animations** - Subtle hover effects, loading states, and micro-interactions
- ✅ **Enhanced Cards** - Professional project cards, feature cards, stats cards
- ✅ **Form Components** - Professional contact form with validation and loading states
- ✅ **Badge System** - Status indicators, skill badges, and content tags
- ✅ **Progress Bars** - Animated skill progress indicators
- ✅ **Interactive Elements** - Tooltips, toasts, skeleton loading states
- ✅ **Mobile-First Design** - Responsive layout optimized for all screen sizes
- ✅ **Hero Sections** - Consistent, professional landing sections across all pages
- ✅ **Interactive Contact Form** - HTMX-powered with email integration
- ✅ **Project Portfolio** - Enhanced showcase of professional work
- ✅ **Blog System** - Professional blog layout with tagging and filtering
- ✅ **FastAPI Backend** - Modern Python web framework
- ✅ **HTMX Integration** - Dynamic interactions without JavaScript frameworks
- ✅ **Email Service** - Async email sending with production/dev modes
- ✅ **SEO Optimized** - Meta tags, structured data, and canonical URLs
- ✅ **Testing Suite** - Pytest + Puppeteer for E2E testing

### Documentation
- Comprehensive README with feature list and setup instructions
- Design system documentation with component library
- Contact form setup guide
- Development roadmap and architecture documentation

### Testing
- E2E testing with Puppeteer
- Comprehensive screenshot testing across devices
- Dark mode testing suite
- Contact form validation testing

## Code Review Findings - 2025-01-08

### Security Issues Identified
- **HIGH**: XSS vulnerabilities in email HTML generation (`app/services/email.py`)
- **HIGH**: Weak default SECRET_KEY (`app/config.py`)
- **MEDIUM**: Information disclosure in error messages (`app/routers/api.py`)
- **MEDIUM**: Missing rate limiting on contact form
- **MEDIUM**: No CSRF protection for forms
- **MEDIUM**: Input length validation missing

### Code Quality Issues Identified
- **HIGH**: Massive code duplication in project data (`app/routers/api.py`)
- **MEDIUM**: Missing logging framework (using print statements)
- **MEDIUM**: Hardcoded sample data in service classes
- **LOW**: Missing type hints in Settings class
- **LOW**: Inconsistent HTML string formatting

### Performance Issues Identified
- **MEDIUM**: Inefficient related posts algorithm (O(n²) complexity)
- **MEDIUM**: No caching layer implemented
- **LOW**: Potential ID collision in blog service

### Architecture Issues Identified
- **HIGH**: No proper data persistence layer
- **MEDIUM**: Mixed development/production code
- **MEDIUM**: Hardcoded configuration values

## Template for Future Releases

```markdown
## [Version] - YYYY-MM-DD

### Added
- New features and capabilities

### Changed
- Changes to existing functionality

### Deprecated
- Features that will be removed in future versions

### Removed
- Features that have been removed

### Fixed
- Bug fixes and corrections

### Security
- Security improvements and vulnerability fixes

### Performance
- Performance improvements and optimizations

### Documentation
- Documentation updates and improvements

### Testing
- Testing improvements and new test coverage
```

## Change Categories

### Priority Levels
- **Critical**: Security vulnerabilities, data loss risks
- **High**: Performance issues, major bugs, architecture problems
- **Medium**: Code quality, maintenance issues, minor bugs
- **Low**: Documentation, code style, optimization

### Change Types
- **Security**: Vulnerability fixes, security enhancements
- **Performance**: Speed improvements, optimization
- **Feature**: New functionality, capabilities
- **Bug**: Fixes to existing functionality
- **Refactor**: Code organization, architecture improvements
- **Documentation**: README, guides, comments
- **Testing**: Test coverage, testing infrastructure
- **CI/CD**: Build, deployment, automation improvements

## Tracking Progress

### Issue Status
- ⭕ **Open**: Issue identified, not yet started
- 🔄 **In Progress**: Currently being worked on
- ✅ **Completed**: Issue resolved and tested
- 🚫 **Blocked**: Cannot proceed due to dependencies
- 📋 **Review**: Code complete, awaiting review

### Review Schedule
- **Daily**: Check critical security issues
- **Weekly**: Review high priority items
- **Monthly**: Assess medium/long-term improvements
- **Quarterly**: Full security audit and architecture review

---

**Maintained by**: Development Team
**Last Updated**: 2026-02-15
**Next Review**: 2026-03-01
