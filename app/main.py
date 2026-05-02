"""FastAPI application entry point for CareerPath AI Bob.

Configures logging, initialises the database, seeds demo data, mounts
static files, registers all routers, and provides root and health endpoints.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.database import get_db, init_db
from app.logging_config import configure_logging
from app.routers import (
    analytics,
    assignments,
    business_units,
    career_path_requirements,
    career_paths,
    employee_skills,
    employees,
    enrollments,
    industry_standards,
    learning_resources,
    projects,
    skills,
)
from app.seed import run_if_empty

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application startup and shutdown lifecycle.

    On startup: configure logging, initialise database tables, seed demo data.
    On shutdown: log clean exit message.

    Args:
        app: The FastAPI application instance.
    """
    configure_logging()
    logger.info("CareerPath AI Bob starting up…")
    init_db()
    db = next(get_db())
    try:
        run_if_empty(db)
    finally:
        db.close()
    yield
    logger.info("CareerPath AI Bob shutting down cleanly.")


app = FastAPI(
    title="CareerPath AI Bob",
    description="Enterprise Talent Development & Career Pathing Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers
app.include_router(business_units.router)
app.include_router(employees.router)
app.include_router(projects.router)
app.include_router(assignments.router)
app.include_router(skills.router)
app.include_router(employee_skills.router)
app.include_router(industry_standards.router)
app.include_router(career_paths.router)
app.include_router(career_path_requirements.router)
app.include_router(learning_resources.router)
app.include_router(enrollments.router)
app.include_router(analytics.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Redirect root path to the static dashboard.

    Returns:
        RedirectResponse: 302 redirect to /static/index.html.
    """
    return RedirectResponse(url="/static/index.html")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Application health probe.

    Returns:
        dict: Status object confirming the API is running.
    """
    return {"status": "ok"}
