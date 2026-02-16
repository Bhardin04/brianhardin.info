"""Shared test fixtures.

Sets USE_DATABASE=False so public-route tests use in-memory services
instead of requiring a live database.  The DB path is exercised separately
in tests/test_database.py and the admin test files.
"""

import pytest

from app.config import settings


@pytest.fixture(autouse=True)
def _use_in_memory_services():
    """Disable database routing for tests that don't set up their own DB."""
    original = settings.USE_DATABASE
    settings.USE_DATABASE = False
    yield
    settings.USE_DATABASE = original
