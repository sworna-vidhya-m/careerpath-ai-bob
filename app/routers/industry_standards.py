"""Industry Standards router providing CRUD endpoints for IndustryStandardSkill entities."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import DuplicateError, NotFoundError, raise_http_from_app_exception
from app.models import IndustryStandardSkill
from app.schemas import (
    IndustryStandardSkillCreate,
    IndustryStandardSkillRead,
    IndustryStandardSkillUpdate,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/industry-standards", tags=["industry-standards"])

MAX_LIMIT = 500


def _get_or_404(db: Session, iss_id: int) -> IndustryStandardSkill:
    """Retrieve an IndustryStandardSkill by id or raise NotFoundError.

    Args:
        db: Active database session.
        iss_id: Primary key.
    """
    iss = db.query(IndustryStandardSkill).filter(IndustryStandardSkill.id == iss_id).first()
    if not iss:
        raise NotFoundError(f"IndustryStandardSkill {iss_id} not found.")
    return iss


@router.get("/", response_model=List[IndustryStandardSkillRead])
def list_industry_standards(
    skip: int = 0,
    limit: int = 100,
    business_unit_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
) -> List[IndustryStandardSkill]:
    """Return a paginated list of industry standard skills with optional BU filter.

    Args:
        skip: Offset for pagination.
        limit: Maximum results (capped at 500).
        business_unit_id: Filter by business unit.
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    query = db.query(IndustryStandardSkill)
    if business_unit_id is not None:
        query = query.filter(IndustryStandardSkill.business_unit_id == business_unit_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{iss_id}", response_model=IndustryStandardSkillRead)
def get_industry_standard(iss_id: int, db: Session = Depends(get_db)) -> IndustryStandardSkill:
    """Retrieve a single industry standard skill by id.

    Args:
        iss_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, iss_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=IndustryStandardSkillRead, status_code=201)
def create_industry_standard(
    payload: IndustryStandardSkillCreate, db: Session = Depends(get_db)
) -> IndustryStandardSkill:
    """Create a new industry standard skill entry.

    Args:
        payload: Validated creation payload.
        db: Injected database session.

    Raises:
        HTTPException 409: If this BU-skill pair already exists.
    """
    iss = IndustryStandardSkill(**payload.model_dump())
    db.add(iss)
    try:
        db.commit()
        db.refresh(iss)
        logger.info("Created IndustryStandardSkill id=%d bu=%d skill=%d", iss.id, iss.business_unit_id, iss.skill_id)
        return iss
    except IntegrityError:
        db.rollback()
        raise_http_from_app_exception(DuplicateError("BU-skill pair already exists."))


@router.put("/{iss_id}", response_model=IndustryStandardSkillRead)
def update_industry_standard(
    iss_id: int, payload: IndustryStandardSkillUpdate, db: Session = Depends(get_db)
) -> IndustryStandardSkill:
    """Update an existing industry standard skill (partial update supported).

    Args:
        iss_id: Primary key.
        payload: Fields to update.
        db: Injected database session.
    """
    try:
        iss = _get_or_404(db, iss_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(iss, field, value)
    try:
        db.commit()
        db.refresh(iss)
        logger.info("Updated IndustryStandardSkill id=%d", iss_id)
        return iss
    except IntegrityError:
        db.rollback()
        raise_http_from_app_exception(DuplicateError("BU-skill pair already exists."))


@router.delete("/{iss_id}", status_code=204)
def delete_industry_standard(iss_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an industry standard skill entry by id.

    Args:
        iss_id: Primary key.
        db: Injected database session.
    """
    try:
        iss = _get_or_404(db, iss_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(iss)
    db.commit()
    logger.info("Deleted IndustryStandardSkill id=%d", iss_id)
