"""Pytest fixtures for CareerPath AI Bob test suite.

Overrides the production database dependency with an in-memory SQLite
database that is seeded once per test session. Tests never touch data/app.db.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.seed import run_if_empty

# In-memory SQLite — StaticPool keeps the same connection so tables persist
# across the session without writing to disk.
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> None:
    """Create all tables and seed the in-memory database once per test session.

    This fixture runs automatically before any test in the session. It creates
    the schema and seeds demo data exactly as the production app does at startup.
    """
    # Import models so they are registered with Base.metadata before create_all.
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=test_engine)
    db = TestSessionLocal()
    try:
        run_if_empty(db)
    finally:
        db.close()


def override_get_db():
    """Dependency override that yields a session backed by the in-memory DB."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def client() -> TestClient:
    """Provide a TestClient wired to the in-memory database for the full session.

    Returns:
        TestClient: HTTP client for making requests against the test app.
    """
    return TestClient(app, raise_server_exceptions=True)
