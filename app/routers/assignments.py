"""Assignments router providing CRUD endpoints for ProjectAssignment entities."""

import logging
from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import NotFoundError, raise_http_from_app_exception
from app.models import ProjectAssignment
from app.schemas import ProjectAssignmentCreate, ProjectAssignmentRead, ProjectAssignmentUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/assignments", tags=["assignments"])

MAX_LIMIT = 500


def _get_or_404(db: Session, assignment_id: int) -> ProjectAssignment:
    """Retrieve a ProjectAssignment by id or raise NotFoundError.

    Args:
        db: Active database session.
        assignment_id: Primary key.
    """
    asgn = db.query(ProjectAssignment).filter(ProjectAssignment.id == assignment_id).first()
    if not asgn:
        raise NotFoundError(f"Assignment {assignment_id} not found.")
    return asgn


@router.get("/", response_model=List[ProjectAssignmentRead])
def list_assignments(
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[int] = Query(None),
    project_id: Optional[int] = Query(None),
    active_only: bool = Query(False),
    db: Session = Depends(get_db),
) -> List[ProjectAssignment]:
    """Return a paginated, filtered list of project assignments.

    Args:
        skip: Offset for pagination.
        limit: Maximum results (capped at 500).
        employee_id: Filter by employee.
        project_id: Filter by project.
        active_only: If True, only return assignments with no end_date.
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    query = db.query(ProjectAssignment)
    if employee_id is not None:
        query = query.filter(ProjectAssignment.employee_id == employee_id)
    if project_id is not None:
        query = query.filter(ProjectAssignment.project_id == project_id)
    if active_only:
        query = query.filter(ProjectAssignment.end_date.is_(None))
    return query.offset(skip).limit(limit).all()


@router.get("/{assignment_id}", response_model=ProjectAssignmentRead)
def get_assignment(assignment_id: int, db: Session = Depends(get_db)) -> ProjectAssignment:
    """Retrieve a single assignment by id.

    Args:
        assignment_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, assignment_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=ProjectAssignmentRead, status_code=201)
def create_assignment(
    payload: ProjectAssignmentCreate, db: Session = Depends(get_db)
) -> ProjectAssignment:
    """Create a new project assignment.

    Args:
        payload: Validated creation payload.
        db: Injected database session.
    """
    asgn = ProjectAssignment(**payload.model_dump())
    db.add(asgn)
    db.commit()
    db.refresh(asgn)
    logger.info("Created Assignment id=%d emp=%d proj=%d", asgn.id, asgn.employee_id, asgn.project_id)
    return asgn


@router.put("/{assignment_id}", response_model=ProjectAssignmentRead)
def update_assignment(
    assignment_id: int, payload: ProjectAssignmentUpdate, db: Session = Depends(get_db)
) -> ProjectAssignment:
    """Update an existing assignment (partial update supported).

    Args:
        assignment_id: Primary key.
        payload: Fields to update.
        db: Injected database session.
    """
    try:
        asgn = _get_or_404(db, assignment_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(asgn, field, value)
    db.commit()
    db.refresh(asgn)
    logger.info("Updated Assignment id=%d", assignment_id)
    return asgn


@router.delete("/{assignment_id}", status_code=204)
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an assignment by id.

    Args:
        assignment_id: Primary key.
        db: Injected database session.
    """
    try:
        asgn = _get_or_404(db, assignment_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(asgn)
    db.commit()
    logger.info("Deleted Assignment id=%d", assignment_id)
