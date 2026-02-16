# Development Roadmap

> **Last Updated**: 2026-02-16
> **Current Version**: Unreleased (post-v1.4.0)
> **Test Suite**: 164 tests passing

## Completed Phases

### Phase 1: Foundation (v1.0.0 - v1.2.0)
- [x] Design system with 150+ CSS tokens
- [x] Responsive mobile-first layout
- [x] Interactive contact form with HTMX
- [x] Dark mode support
- [x] Professional resume page
- [x] SEO meta tags and structured data
- [x] Project portfolio with case studies

### Phase 2: Interactive Demos & Content (v1.3.0 - v1.4.0)
- [x] Payment processing demo with WebSocket real-time updates
- [x] NetSuite to SAP data pipeline demo
- [x] Sales & revenue dashboard demo
- [x] Collections management dashboard demo
- [x] Blog system with tagging and RSS feed
- [x] Comprehensive case study data for all projects
- [x] CI/CD pipeline with GitHub Actions

### Phase 3: Security & Quality
- [x] Rate limiting on all endpoints (slowapi)
- [x] CSRF protection with HMAC-signed tokens
- [x] Input validation and XSS prevention
- [x] SMTP header injection fix
- [x] Pydantic V2 migration (ConfigDict, .model_dump())
- [x] Starlette TemplateResponse updated to new API
- [x] Demo session limits (MAX_SESSIONS=100, TTL=1hr)
- [x] WebSocket connection limits (200 total, 5/session)
- [x] ProjectService as single source of truth
- [x] Demo test suite (37 tests)
- [x] Pre-commit hooks (ruff, mypy, bandit)

### Phase 4: Admin Panel / CMS
- [x] Database foundation (SQLAlchemy 2.0 async, PostgreSQL + SQLite)
- [x] GitHub OAuth authentication with session management
- [x] Admin dashboard with sidebar navigation and dark mode
- [x] Blog CRUD management (create, edit, delete, publish toggle, markdown)
- [x] Project CRUD management (with case study data)
- [x] Contact message inbox (view, mark read, archive, delete)
- [x] Site settings management (key-value store)
- [x] Data seeding script (`python -m app.scripts.seed`)
- [x] Feature-flagged DB migration for public routes (`USE_DATABASE`)
- [x] Database-backed sitemap with dynamic project/blog URLs
- [x] 164 tests passing with full pre-commit compliance

---

## Current Backlog

### MEDIUM Priority Improvements

See [improvements-list.md](improvements-list.md) for full details on each item.

#### Batch 1: Security & Quick Wins
- [ ] **M1** - Security response headers middleware
- [ ] **M2** - Typed Pydantic models for demo POST bodies
- [ ] **M3** - Constrain analytics/error report payloads
- [ ] **M6** - Tests for error handlers, sitemap, RSS feed

#### Batch 2: Test Coverage & Configuration
- [ ] **M4** - WebSocket service test coverage (currently 43%)
- [ ] **M5** - Configure structured logging
- [ ] **M11** - Convert Settings to Pydantic BaseSettings
- [ ] **M12** - EmailService should use Settings
- [ ] **M13** - Blog and project router edge-case tests

#### Batch 3: Cleanup & Polish
- [ ] **M8** - Remove duplicate health check endpoints
- [ ] **M10** - Fix docker-compose deprecations
- [ ] **M14** - Replace deprecated asyncio.get_event_loop()
- [ ] **M15** - Consolidate Jinja2Templates instances

---

## Future Phases

### Phase 5: Production Hardening
- [ ] Structured JSON logging for production
- [ ] Pydantic BaseSettings for all configuration
- [ ] Error monitoring (Sentry or similar)
- [ ] Performance monitoring / APM
- [ ] CDN for static assets
- [ ] Gzip/brotli compression

### Phase 6: Advanced Features
- [ ] Redis caching layer
- [ ] Accessibility audit (WCAG compliance)
- [ ] Visual regression testing
- [ ] Load testing

---

## Key Decisions

| Decision | Rationale | Date |
|----------|-----------|------|
| PostgreSQL (prod) + SQLite (dev) | Render has ephemeral filesystems; PostgreSQL persists. SQLAlchemy abstracts the difference. | 2026-02-16 |
| Feature-flagged DB migration | `USE_DATABASE` env var allows zero-risk rollout; in-memory services remain as fallback. | 2026-02-16 |
| Session tokens in DB (not JWT) | Enables server-side invalidation (logout, expiry cleanup). | 2026-02-16 |
| Standalone admin base template | Prevents admin sidebar/nav from leaking into public site. | 2026-02-16 |
| JSON columns for nested project data | Avoids 4+ extra tables for data always read/written as a unit. | 2026-02-16 |
| Keep Tailwind CDN | Production build broke CSS due to `styles.css` broad selectors overriding Tailwind utilities. | 2026-02-16 |
| ProjectService pattern | Eliminated duplicate project data in 3 files. Single source of truth. | 2026-02-16 |
| Skip Pydantic BaseSettings for now | Works but requires `pydantic-settings` dependency. Planned for Batch 2. | 2026-02-16 |
