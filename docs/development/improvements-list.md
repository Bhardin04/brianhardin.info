# Code Review Improvements List

> **Last Updated**: 2026-02-16
> **Project**: brianhardin.info Personal Website
> **Test Suite**: 164 tests passing, ruff clean, mypy clean

## Completed Items

### HIGH Priority (All Complete)

| ID | Issue | Files | Status |
|----|-------|-------|--------|
| H1 | SMTP header injection vulnerability | `app/services/email.py` | ✅ Fixed - strips `\r\n` from subject |
| H2 | Pydantic V1 deprecated APIs (`.dict()`, `class Config`) | `app/models/project.py`, `app/services/demo.py`, `app/routers/demos.py` | ✅ Migrated to `.model_dump()` and `ConfigDict` |
| H3 | Starlette TemplateResponse deprecated signature | All routers, `app/main.py` | ✅ Updated to `TemplateResponse(request, template, context=)` |
| H4 | Unbounded demo session memory (DoS vector) | `app/services/demo.py` | ✅ Added MAX_SESSIONS=100, TTL=1hr |
| H5 | Duplicate project data across 3 files | `app/routers/api.py`, `app/routers/projects.py`, `app/main.py` | ✅ Consolidated into `app/services/project.py` |
| H6 | No tests for demo endpoints (~600 lines untested) | `tests/test_demos.py` | ✅ Added 37 tests |
| H7 | Tailwind CDN → production build | `app/templates/base.html` | ❌ Skipped - broke CSS, reverted. Keeping CDN. |

### Previously Completed (v1.3.0 and earlier)

| ID | Issue | Status |
|----|-------|--------|
| SEC-001 | XSS in email HTML generation | ✅ Fixed with `html.escape()` |
| SEC-002 | Weak default SECRET_KEY | ✅ Replaced with `secrets.token_urlsafe(32)` |
| SEC-003 | Information disclosure in error messages | ✅ Generic errors for users, detailed logging |
| SEC-004 | Unescaped user input in email | ✅ All inputs escaped |
| SEC-005 | Missing rate limiting | ✅ Added via `slowapi` on all endpoints |
| SEC-006 | No CSRF protection | ✅ Double Submit Cookie with HMAC-signed tokens |
| SEC-007 | Input length validation missing | ✅ Pydantic field constraints added |
| CQ-001 | Project data duplication | ✅ Consolidated into ProjectService |

---

## MEDIUM Priority (Current Backlog)

### Batch 1: Security & Quick Wins

#### M1. Add Security Response Headers Middleware
- **Category**: Security
- **Effort**: Small (1-2 hours)
- **Files**: `app/main.py`, `app/middleware.py`
- **Status**: ⭕ Open

The application serves no security headers on responses. Missing headers include `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, `Referrer-Policy`, and `Permissions-Policy`. The `base.html` has a meta referrer tag but that only covers HTML pages.

**Implementation**:
```python
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if not settings.DEBUG:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

---

#### M2. Replace Untyped `dict[str, Any]` Demo POST Bodies with Pydantic Models
- **Category**: Security / Code Quality
- **Effort**: Medium (2-3 hours)
- **Files**: `app/routers/demos.py` (lines ~112, ~219, ~290, ~353)
- **Status**: ⭕ Open

Four demo POST endpoints accept raw `dict[str, Any]` bodies instead of typed Pydantic models:
- `process_payment` - should accept `ProcessPaymentRequest(session_id, payment)`
- `extract_pipeline_data` - should accept `PipelineExtractRequest(session_id, params)`
- `get_dashboard_data` - should accept `DashboardDataRequest(session_id, period)`
- `get_collections_data` - should accept `CollectionsDataRequest(session_id)`

This bypasses FastAPI's validation, produces no OpenAPI schema, and allows malformed payloads to reach business logic.

---

#### M3. Constrain Analytics/Error Report Payloads
- **Category**: Security / Code Quality
- **Effort**: Small (1 hour)
- **Files**: `app/routers/api.py` (analytics and error-report endpoints)
- **Status**: ⭕ Open

`/api/analytics` and `/api/error-report` accept `dict[str, str]` with no size constraints. An attacker could send arbitrarily large payloads that get logged directly, potentially exhausting disk/memory.

**Implementation**: Create constrained Pydantic models:
```python
class AnalyticsEvent(BaseModel):
    event: str = Field(max_length=100)
    page: str = Field(default="", max_length=200)
    data: dict[str, str] = Field(default_factory=dict)
```

---

#### M6. Add Tests for Error Handlers, Sitemap, RSS Feed
- **Category**: Test Coverage
- **Effort**: Small (1-2 hours)
- **Files**: `tests/test_main.py`
- **Status**: ⭕ Open

`main.py` has 67% coverage. Untested paths include:
- 404 error handler (custom template rendering)
- 500 error handler (including fallback path)
- Sitemap XML generation (`/sitemap.xml`)
- Service worker endpoint (`/service-worker.js`)
- Blog RSS feed (`/blog/feed.xml`)

---

#### M7. Dynamic Project IDs in Sitemap
- **Category**: Maintainability
- **Effort**: Small (30 minutes)
- **Files**: `app/main.py` (line ~115)
- **Status**: ✅ Fixed (via Phase 7 DB migration)

When `USE_DATABASE=true`, sitemap reads project IDs from the database dynamically. Hardcoded IDs remain as fallback when `USE_DATABASE=false`.

---

### Batch 2: Test Coverage & Configuration

#### M4. Improve WebSocket Service Test Coverage (Currently 43%)
- **Category**: Test Coverage
- **Effort**: Medium (3-4 hours)
- **Files**: `app/services/websocket.py`, `tests/test_demos.py`
- **Status**: ⭕ Open

Lowest coverage in the codebase. Untested paths:
- Connection limit enforcement (`MAX_CONNECTIONS`, `MAX_CONNECTIONS_PER_SESSION`)
- `disconnect()` cleanup logic
- `send_to_session()` and `broadcast_to_demo_type()`
- All `RealtimeDataSimulator` simulation methods
- Error paths in `send_to_connection()`

---

#### M5. Configure Structured Logging
- **Category**: Observability
- **Effort**: Small (1-2 hours)
- **Files**: `app/main.py`
- **Status**: ⭕ Open

The app uses `logging.getLogger(__name__)` but never configures the logging system. No log level config, no format, no structured output. f-string log calls (`logger.error(f"Error: {str(e)}")`) are evaluated even when that level is disabled.

**Implementation**:
- Add `logging.basicConfig()` or `dictConfig` in `main.py`
- JSON output for production, human-readable for dev
- Convert f-string log calls to lazy formatting: `logger.error("Error: %s", e)`

---

#### M11. Convert Settings to Pydantic BaseSettings
- **Category**: Code Quality
- **Effort**: Small (1 hour)
- **Files**: `app/config.py`
- **Status**: ⭕ Open

`Settings` class manually reads env vars with `os.getenv()` and inline type conversion. A non-numeric `SMTP_PORT` would crash with an unhelpful `ValueError`. Pydantic `BaseSettings` handles this automatically with validation.

**Implementation**: Requires adding `pydantic-settings` dependency:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    SMTP_PORT: int = 587
    model_config = ConfigDict(env_file=".env")
```

---

#### M12. EmailService Should Use Settings, Not `os.getenv()`
- **Category**: Maintainability
- **Effort**: Small (30 minutes)
- **Files**: `app/services/email.py` (lines 16-21)
- **Status**: ⭕ Open

`EmailService.__init__()` reads `os.getenv()` directly, duplicating what `app.config.Settings` already stores. Two independent sources of truth for email configuration.

**Fix**: Import and use the `settings` instance:
```python
from app.config import settings

class EmailService:
    def __init__(self) -> None:
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
```

---

#### M13. Blog and Project Router Edge-Case Tests
- **Category**: Test Coverage
- **Effort**: Small (1-2 hours)
- **Files**: `tests/test_blog.py`, `tests/test_main.py`
- **Status**: ⭕ Open

Missing coverage:
- `blog.py` line 99: Accessing unpublished blog post returns 404
- `blog.py` line 111: Related posts logic with shared tags
- `blog.py` lines 132-134: API blog posts with tag filter + `published_only=False`
- `projects.py`: API `get_project()` 404 for non-existent project ID

---

### Batch 3: Cleanup & Polish

#### M8. Remove Duplicate Health Check Endpoints
- **Category**: Code Quality
- **Effort**: Small (30 minutes)
- **Files**: `app/main.py`, `app/routers/api.py`
- **Status**: ⭕ Open

Duplicate endpoints: `GET /health` (main.py) and `GET /api/health` + `HEAD /api/health` (api.py) return identical responses. Keep `/health` (used by Render) and `/api/ping` (frontend keepalive). Remove `/api/health`.

---

#### M9. Wire Up Markdown Blog Loading or Remove Dead Code
- **Category**: Architecture / Technical Debt
- **Effort**: Medium (3-4 hours)
- **Files**: `app/services/blog.py`
- **Status**: ✅ Superseded (by admin CMS)

Blog content is now managed through the admin CMS with database storage (`BlogServiceDB`). The in-memory `BlogService` with hardcoded posts remains as a fallback when `USE_DATABASE=false`. Dead markdown file loading code can be removed in Phase 8 cleanup.

---

#### M10. Fix Docker Compose Deprecations
- **Category**: Infrastructure
- **Effort**: Small (30 minutes)
- **Files**: `docker-compose.yml`
- **Status**: ⭕ Open

1. `version: '3.8'` is deprecated in Docker Compose v2+; remove it
2. Volume mount `- .:/app` mounts entire repo (`.git`, `.env`, etc.) into container; restrict to `./app:/app/app` for production

---

#### M14. Replace Deprecated `asyncio.get_event_loop()` Calls
- **Category**: Code Quality
- **Effort**: Small (30 minutes)
- **Files**: `app/services/websocket.py` (8 occurrences)
- **Status**: ⭕ Open

`asyncio.get_event_loop()` is deprecated in Python 3.12+. Used solely for timestamps (`asyncio.get_event_loop().time()`). Replace with `time.time()`.

---

#### M15. Consolidate Jinja2Templates Instances
- **Category**: Code Quality
- **Effort**: Small (1 hour)
- **Files**: `app/main.py`, `app/routers/pages.py`, `app/routers/demos.py`, `app/routers/blog.py`, `app/routers/projects.py`
- **Status**: ⭕ Open

`Jinja2Templates(directory="app/templates")` is instantiated 5 times. Each creates its own template loader and Jinja2 environment. Creates duplicate memory usage and makes it impossible to add global template variables in one place.

**Fix**: Create shared instance in `app/dependencies.py` and import everywhere.

---

## Summary Table

| # | Item | Category | Effort | Impact | Status |
|---|------|----------|--------|--------|--------|
| **Batch 1** | | | | | |
| M1 | Security response headers | Security | Small | High | ⭕ Open |
| M2 | Typed Pydantic models for demo POST bodies | Security/Quality | Medium | High | ⭕ Open |
| M3 | Constrain analytics/error report payloads | Security/Quality | Small | Medium | ⭕ Open |
| M6 | Test error handlers, sitemap, RSS feed | Testing | Small | Medium | ⭕ Open |
| M7 | Dynamic project IDs in sitemap | Maintainability | Small | Low | ✅ Fixed |
| **Batch 2** | | | | | |
| M4 | WebSocket service test coverage (43%) | Testing | Medium | High | ⭕ Open |
| M5 | Configure structured logging | Observability | Small | Medium | ⭕ Open |
| M11 | Convert Settings to Pydantic BaseSettings | Code Quality | Small | Medium | ⭕ Open |
| M12 | EmailService should use Settings | Maintainability | Small | Low | ⭕ Open |
| M13 | Blog and project router edge-case tests | Testing | Small | Medium | ⭕ Open |
| **Batch 3** | | | | | |
| M8 | Remove duplicate health check endpoints | Code Quality | Small | Low | ⭕ Open |
| M9 | Wire up markdown blog or remove dead code | Architecture | Medium | Medium | ✅ Superseded |
| M10 | Fix docker-compose deprecations | Infrastructure | Small | Low | ⭕ Open |
| M14 | Replace deprecated asyncio.get_event_loop() | Code Quality | Small | Low | ⭕ Open |
| M15 | Consolidate Jinja2Templates instances | Code Quality | Small | Low | ⭕ Open |

**Total estimated effort**: ~20-25 hours across all 15 items.
**Batch 1 alone**: ~5-7 hours for highest-impact improvements.

---

**Next Review**: 2026-03-01
