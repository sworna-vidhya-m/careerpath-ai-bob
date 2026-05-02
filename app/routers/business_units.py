"""Business Units router providing CRUD endpoints for BusinessUnit entities."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import NotFoundError, DuplicateError, raise_http_from_app_exception
from app.models import BusinessUnit
from app.schemas import BusinessUnitCreate, BusinessUnitRead, BusinessUnitUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/business-units", tags=["business-units"])

MAX_LIMIT = 500


def _get_or_404(db: Session, bu_id: int) -> BusinessUnit:
    """Retrieve a BusinessUnit by id or raise NotFoundError.

    Args:
        db: Active database session.
        bu_id: Primary key of the BusinessUnit.

    Returns:
        The matching BusinessUnit ORM instance.

    Raises:
        NotFoundError: If no BusinessUnit with the given id exists.
    """
    bu = db.query(BusinessUnit).filter(BusinessUnit.id == bu_id).first()
    if not bu:
        raise NotFoundError(f"BusinessUnit {bu_id} not found.")
    return bu


@router.get("/", response_model=List[BusinessUnitRead])
def list_business_units(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[BusinessUnit]:
    """Return a paginated list of all business units.

    Args:
        skip: Number of records to skip.
        limit: Maximum records to return (capped at 500).
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    return db.query(BusinessUnit).offset(skip).limit(limit).all()


@router.get("/{bu_id}", response_model=BusinessUnitRead)
def get_business_unit(bu_id: int, db: Session = Depends(get_db)) -> BusinessUnit:
    """Retrieve a single business unit by id.

    Args:
        bu_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, bu_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=BusinessUnitRead, status_code=201)
def create_business_unit(
    payload: BusinessUnitCreate, db: Session = Depends(get_db)
) -> BusinessUnit:
    """Create a new business unit.

    Args:
        payload: Validated creation payload.
        db: Injected database session.

    Raises:
        HTTPException 409: If a business unit with the same name already exists.
    """
    bu = BusinessUnit(**payload.model_dump())
    db.add(bu)
    try:
        db.commit()
        db.refresh(bu)
        logger.info("Created BusinessUnit id=%d name=%s", bu.id, bu.name)
        return bu
    except IntegrityError as exc:
        db.rollback()
        raise_http_from_app_exception(DuplicateError(f"BusinessUnit name '{payload.name}' already exists."))


@router.put("/{bu_id}", response_model=BusinessUnitRead)
def update_business_unit(
    bu_id: int, payload: BusinessUnitUpdate, db: Session = Depends(get_db)
) -> BusinessUnit:
    """Update an existing business unit (partial update supported).

    Args:
        bu_id: Primary key of the business unit to update.
        payload: Fields to update; unset fields are ignored.
        db: Injected database session.
    """
    try:
        bu = _get_or_404(db, bu_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(bu, field, value)
    try:
        db.commit()
        db.refresh(bu)
        logger.info("Updated BusinessUnit id=%d", bu_id)
        return bu
    except IntegrityError as exc:
        db.rollback()
        raise_http_from_app_exception(DuplicateError("BusinessUnit name already in use."))


@router.delete("/{bu_id}", status_code=204)
def delete_business_unit(bu_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a business unit by id.

    Args:
        bu_id: Primary key of the business unit to delete.
        db: Injected database session.
    """
    try:
        bu = _get_or_404(db, bu_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(bu)
    db.commit()
    logger.info("Deleted BusinessUnit id=%d", bu_id)
