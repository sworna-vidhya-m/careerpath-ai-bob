"""Projects router providing CRUD endpoints for Project entities."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import DuplicateError, NotFoundError, raise_http_from_app_exception
from app.models import Project, ProjectStatus
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/projects", tags=["projects"])

MAX_LIMIT = 500


def _get_or_404(db: Session, project_id: int) -> Project:
    """Retrieve a Project by id or raise NotFoundError.

    Args:
        db: Active database session.
        project_id: Primary key.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise NotFoundError(f"Project {project_id} not found.")
    return project


@router.get("/", response_model=List[ProjectRead])
def list_projects(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ProjectStatus] = Query(None),
    db: Session = Depends(get_db),
) -> List[Project]:
    """Return a paginated list of projects with optional status filter.

    Args:
        skip: Offset for pagination.
        limit: Maximum results (capped at 500).
        status: Optional ProjectStatus filter.
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    query = db.query(Project)
    if status is not None:
        query = query.filter(Project.status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)) -> Project:
    """Retrieve a single project by id.

    Args:
        project_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, project_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> Project:
    """Create a new project.

    Args:
        payload: Validated creation payload.
        db: Injected database session.
    """
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    logger.info("Created Project id=%d name=%s", project.id, project.name)
    return project


@router.put("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)
) -> Project:
    """Update an existing project (partial update supported).

    Args:
        project_id: Primary key.
        payload: Fields to update.
        db: Injected database session.
    """
    try:
        project = _get_or_404(db, project_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    logger.info("Updated Project id=%d", project_id)
    return project


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a project by id.

    Args:
        project_id: Primary key.
        db: Injected database session.
    """
    try:
        project = _get_or_404(db, project_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(project)
    db.commit()
    logger.info("Deleted Project id=%d", project_id)
