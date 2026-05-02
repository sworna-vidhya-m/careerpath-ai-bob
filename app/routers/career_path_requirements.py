"""Career Path Requirements router providing CRUD for CareerPathSkillRequirement entities."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import DuplicateError, NotFoundError, raise_http_from_app_exception
from app.models import CareerPathSkillRequirement
from app.schemas import (
    CareerPathSkillRequirementCreate,
    CareerPathSkillRequirementRead,
    CareerPathSkillRequirementUpdate,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/career-path-requirements", tags=["career-path-requirements"])

MAX_LIMIT = 500


def _get_or_404(db: Session, req_id: int) -> CareerPathSkillRequirement:
    """Retrieve a CareerPathSkillRequirement by id or raise NotFoundError.

    Args:
        db: Active database session.
        req_id: Primary key.
    """
    req = db.query(CareerPathSkillRequirement).filter(
        CareerPathSkillRequirement.id == req_id
    ).first()
    if not req:
        raise NotFoundError(f"CareerPathSkillRequirement {req_id} not found.")
    return req


@router.get("/", response_model=List[CareerPathSkillRequirementRead])
def list_career_path_requirements(
    skip: int = 0,
    limit: int = 100,
    career_path_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
) -> List[CareerPathSkillRequirement]:
    """Return a paginated list of career path skill requirements.

    Args:
        skip: Offset for pagination.
        limit: Maximum results (capped at 500).
        career_path_id: Filter by career path.
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    query = db.query(CareerPathSkillRequirement)
    if career_path_id is not None:
        query = query.filter(CareerPathSkillRequirement.career_path_id == career_path_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{req_id}", response_model=CareerPathSkillRequirementRead)
def get_career_path_requirement(
    req_id: int, db: Session = Depends(get_db)
) -> CareerPathSkillRequirement:
    """Retrieve a single career path requirement by id.

    Args:
        req_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, req_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=CareerPathSkillRequirementRead, status_code=201)
def create_career_path_requirement(
    payload: CareerPathSkillRequirementCreate, db: Session = Depends(get_db)
) -> CareerPathSkillRequirement:
    """Create a new career path skill requirement.

    Args:
        payload: Validated creation payload.
        db: Injected database session.

    Raises:
        HTTPException 409: If this career-path/skill pair already exists.
    """
    req = CareerPathSkillRequirement(**payload.model_dump())
    db.add(req)
    try:
        db.commit()
        db.refresh(req)
        logger.info("Created CareerPathSkillRequirement id=%d path=%d skill=%d", req.id, req.career_path_id, req.skill_id)
        return req
    except IntegrityError:
        db.rollback()
        raise_http_from_app_exception(DuplicateError("Career-path/skill pair already exists."))


@router.put("/{req_id}", response_model=CareerPathSkillRequirementRead)
def update_career_path_requirement(
    req_id: int, payload: CareerPathSkillRequirementUpdate, db: Session = Depends(get_db)
) -> CareerPathSkillRequirement:
    """Update an existing career path requirement (partial update supported).

    Args:
        req_id: Primary key.
        payload: Fields to update.
        db: Injected database session.
    """
    try:
        req = _get_or_404(db, req_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(req, field, value)
    try:
        db.commit()
        db.refresh(req)
        logger.info("Updated CareerPathSkillRequirement id=%d", req_id)
        return req
    except IntegrityError:
        db.rollback()
        raise_http_from_app_exception(DuplicateError("Career-path/skill pair already exists."))


@router.delete("/{req_id}", status_code=204)
def delete_career_path_requirement(req_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a career path requirement by id.

    Args:
        req_id: Primary key.
        db: Injected database session.
    """
    try:
        req = _get_or_404(db, req_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(req)
    db.commit()
    logger.info("Deleted CareerPathSkillRequirement id=%d", req_id)
