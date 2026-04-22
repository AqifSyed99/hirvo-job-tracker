"""Shared pytest fixtures for backend tests."""

import pytest

from backend.app import create_app, db as _db
from backend.config import TestConfig


@pytest.fixture(scope="session")
def app():
    """Create a Flask app configured for testing (in-memory SQLite)."""
    application = create_app(TestConfig)
    return application


@pytest.fixture(scope="session")
def _db_setup(app):
    """Create all tables once per test session."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()


@pytest.fixture()
def db(app, _db_setup):
    """Provide a clean database transaction for each test (rolled back after)."""
    with app.app_context():
        connection = _db_setup.engine.connect()
        transaction = connection.begin()

        # Bind the session to this connection so we can roll back
        _db_setup.session.bind = connection

        yield _db_setup

        _db_setup.session.remove()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(app, db):
    """Flask test client with a clean DB for each test."""
    return app.test_client()
