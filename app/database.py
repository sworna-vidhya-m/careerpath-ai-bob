"""Database engine, session factory, and table initialisation for CareerPath AI Bob.

Provides:
  - SQLAlchemy engine backed by SQLite
  - Session dependency for FastAPI routes
  - init_db() called at app startup to create tables
"""

import logging
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/app.db"


class Base(DeclarativeBase):
    """SQLAlchemy declarative base shared by all ORM models."""


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and ensures cleanup.

    Yields:
        Session: An active SQLAlchemy session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables in the database if they do not already exist.

    Must be called once at application startup after all models have been
    imported so that Base.metadata is fully populated.
    """
    # Import models here to ensure they are registered with Base.metadata
    # before create_all is called.
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created (or already exist).")
