"""Enrollments router providing CRUD endpoints for LearningEnrollment entities."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import NotFoundError, raise_http_from_app_exception
from app.models import EnrollmentStatus, LearningEnrollment
from app.schemas import LearningEnrollmentCreate, LearningEnrollmentRead, LearningEnrollmentUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/enrollments", tags=["enrollments"])

MAX_LIMIT = 500


def _get_or_404(db: Session, enrollment_id: int) -> LearningEnrollment:
    """Retrieve a LearningEnrollment by id or raise NotFoundError.

    Args:
        db: Active database session.
        enrollment_id: Primary key.
    """
    enroll = db.query(LearningEnrollment).filter(
        LearningEnrollment.id == enrollment_id
    ).first()
    if not enroll:
        raise NotFoundError(f"LearningEnrollment {enrollment_id} not found.")
    return enroll


@router.get("/", response_model=List[LearningEnrollmentRead])
def list_enrollments(
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[int] = Query(None),
    status: Optional[EnrollmentStatus] = Query(None),
    db: Session = Depends(get_db),
) -> List[LearningEnrollment]:
    """Return a paginated list of learning enrollments with optional filters.

    Args:
        skip: Offset for pagination.
        limit: Maximum results (capped at 500).
        employee_id: Filter by employee.
        status: Filter by enrollment status.
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    query = db.query(LearningEnrollment)
    if employee_id is not None:
        query = query.filter(LearningEnrollment.employee_id == employee_id)
    if status is not None:
        query = query.filter(LearningEnrollment.status == status)
    return query.offset(skip).limit(limit).all()


@router.get("/{enrollment_id}", response_model=LearningEnrollmentRead)
def get_enrollment(enrollment_id: int, db: Session = Depends(get_db)) -> LearningEnrollment:
    """Retrieve a single enrollment by id.

    Args:
        enrollment_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, enrollment_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=LearningEnrollmentRead, status_code=201)
def create_enrollment(
    payload: LearningEnrollmentCreate, db: Session = Depends(get_db)
) -> LearningEnrollment:
    """Create a new learning enrollment.

    Args:
        payload: Validated creation payload.
        db: Injected database session.
    """
    enroll = LearningEnrollment(**payload.model_dump())
    db.add(enroll)
    db.commit()
    db.refresh(enroll)
    logger.info("Created LearningEnrollment id=%d emp=%d res=%d", enroll.id, enroll.employee_id, enroll.resource_id)
    return enroll


@router.put("/{enrollment_id}", response_model=LearningEnrollmentRead)
def update_enrollment(
    enrollment_id: int, payload: LearningEnrollmentUpdate, db: Session = Depends(get_db)
) -> LearningEnrollment:
    """Update an existing enrollment (partial update supported).

    Args:
        enrollment_id: Primary key.
        payload: Fields to update.
        db: Injected database session.
    """
    try:
        enroll = _get_or_404(db, enrollment_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(enroll, field, value)
    db.commit()
    db.refresh(enroll)
    logger.info("Updated LearningEnrollment id=%d", enrollment_id)
    return enroll


@router.delete("/{enrollment_id}", status_code=204)
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an enrollment by id.

    Args:
        enrollment_id: Primary key.
        db: Injected database session.
    """
    try:
        enroll = _get_or_404(db, enrollment_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(enroll)
    db.commit()
    logger.info("Deleted LearningEnrollment id=%d", enrollment_id)
