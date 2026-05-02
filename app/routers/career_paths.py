"""Career Paths router providing CRUD endpoints for CareerPath entities."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import NotFoundError, raise_http_from_app_exception
from app.models import CareerPath
from app.schemas import CareerPathCreate, CareerPathRead, CareerPathUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/career-paths", tags=["career-paths"])

MAX_LIMIT = 500


def _get_or_404(db: Session, cp_id: int) -> CareerPath:
    """Retrieve a CareerPath by id or raise NotFoundError.

    Args:
        db: Active database session.
        cp_id: Primary key.
    """
    cp = db.query(CareerPath).filter(CareerPath.id == cp_id).first()
    if not cp:
        raise NotFoundError(f"CareerPath {cp_id} not found.")
    return cp


@router.get("/", response_model=List[CareerPathRead])
def list_career_paths(
    skip: int = 0,
    limit: int = 100,
    business_unit_id: Optional[int] = Query(None),
    from_role: Optional[str] = Query(None),
    db: Session = Depends(get_db),
) -> List[CareerPath]:
    """Return a paginated list of career paths with optional filters.

    Args:
        skip: Offset for pagination.
        limit: Maximum results (capped at 500).
        business_unit_id: Filter by business unit.
        from_role: Filter by source role string.
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    query = db.query(CareerPath)
    if business_unit_id is not None:
        query = query.filter(CareerPath.business_unit_id == business_unit_id)
    if from_role is not None:
        query = query.filter(CareerPath.from_role == from_role)
    return query.offset(skip).limit(limit).all()


@router.get("/{cp_id}", response_model=CareerPathRead)
def get_career_path(cp_id: int, db: Session = Depends(get_db)) -> CareerPath:
    """Retrieve a single career path by id.

    Args:
        cp_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, cp_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=CareerPathRead, status_code=201)
def create_career_path(payload: CareerPathCreate, db: Session = Depends(get_db)) -> CareerPath:
    """Create a new career path.

    Args:
        payload: Validated creation payload.
        db: Injected database session.
    """
    cp = CareerPath(**payload.model_dump())
    db.add(cp)
    db.commit()
    db.refresh(cp)
    logger.info("Created CareerPath id=%d %s->%s", cp.id, cp.from_role, cp.to_role)
    return cp


@router.put("/{cp_id}", response_model=CareerPathRead)
def update_career_path(
    cp_id: int, payload: CareerPathUpdate, db: Session = Depends(get_db)
) -> CareerPath:
    """Update an existing career path (partial update supported).

    Args:
        cp_id: Primary key.
        payload: Fields to update.
        db: Injected database session.
    """
    try:
        cp = _get_or_404(db, cp_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cp, field, value)
    db.commit()
    db.refresh(cp)
    logger.info("Updated CareerPath id=%d", cp_id)
    return cp


@router.delete("/{cp_id}", status_code=204)
def delete_career_path(cp_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a career path by id.

    Args:
        cp_id: Primary key.
        db: Injected database session.
    """
    try:
        cp = _get_or_404(db, cp_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(cp)
    db.commit()
    logger.info("Deleted CareerPath id=%d", cp_id)
