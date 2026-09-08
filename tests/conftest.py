"""Shared test fixtures.

Each test gets its own temporary database file so tests never touch each
other's data or the real study_tracker.db file.
"""

import pytest

from app import create_app


@pytest.fixture
def app(tmp_path):
    """A Flask app pointed at a fresh temporary database."""
    db_path = tmp_path / "test.db"
    app = create_app({"TESTING": True, "DATABASE": str(db_path)})
    yield app


@pytest.fixture
def client(app):
    """A test client for sending requests to the app."""
    return app.test_client()