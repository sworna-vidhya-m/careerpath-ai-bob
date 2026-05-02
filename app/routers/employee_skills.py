"""Employee Skills router providing CRUD endpoints for EmployeeSkill entities."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import DuplicateError, NotFoundError, raise_http_from_app_exception
from app.models import EmployeeSkill
from app.schemas import EmployeeSkillCreate, EmployeeSkillRead, EmployeeSkillUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/employee-skills", tags=["employee-skills"])

MAX_LIMIT = 500


def _get_or_404(db: Session, es_id: int) -> EmployeeSkill:
    """Retrieve an EmployeeSkill by id or raise NotFoundError.

    Args:
        db: Active database session.
        es_id: Primary key.
    """
    es = db.query(EmployeeSkill).filter(EmployeeSkill.id == es_id).first()
    if not es:
        raise NotFoundError(f"EmployeeSkill {es_id} not found.")
    return es


@router.get("/", response_model=List[EmployeeSkillRead])
def list_employee_skills(
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[int] = Query(None),
    skill_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
) -> List[EmployeeSkill]:
    """Return a paginated, filtered list of employee skill records.

    Args:
        skip: Offset for pagination.
        limit: Maximum results (capped at 500).
        employee_id: Filter by employee.
        skill_id: Filter by skill.
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    query = db.query(EmployeeSkill)
    if employee_id is not None:
        query = query.filter(EmployeeSkill.employee_id == employee_id)
    if skill_id is not None:
        query = query.filter(EmployeeSkill.skill_id == skill_id)
    return query.offset(skip).limit(limit).all()


@router.get("/{es_id}", response_model=EmployeeSkillRead)
def get_employee_skill(es_id: int, db: Session = Depends(get_db)) -> EmployeeSkill:
    """Retrieve a single employee skill record by id.

    Args:
        es_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, es_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=EmployeeSkillRead, status_code=201)
def create_employee_skill(
    payload: EmployeeSkillCreate, db: Session = Depends(get_db)
) -> EmployeeSkill:
    """Create a new employee skill record.

    Args:
        payload: Validated creation payload.
        db: Injected database session.

    Raises:
        HTTPException 409: If this employee-skill pair already exists.
    """
    es = EmployeeSkill(**payload.model_dump())
    db.add(es)
    try:
        db.commit()
        db.refresh(es)
        logger.info("Created EmployeeSkill id=%d emp=%d skill=%d", es.id, es.employee_id, es.skill_id)
        return es
    except IntegrityError:
        db.rollback()
        raise_http_from_app_exception(
            DuplicateError("Employee-skill pair already exists.")
        )


@router.put("/{es_id}", response_model=EmployeeSkillRead)
def update_employee_skill(
    es_id: int, payload: EmployeeSkillUpdate, db: Session = Depends(get_db)
) -> EmployeeSkill:
    """Update an existing employee skill record (partial update supported).

    Args:
        es_id: Primary key.
        payload: Fields to update.
        db: Injected database session.
    """
    try:
        es = _get_or_404(db, es_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(es, field, value)
    try:
        db.commit()
        db.refresh(es)
        logger.info("Updated EmployeeSkill id=%d", es_id)
        return es
    except IntegrityError:
        db.rollback()
        raise_http_from_app_exception(DuplicateError("Employee-skill pair already exists."))


@router.delete("/{es_id}", status_code=204)
def delete_employee_skill(es_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an employee skill record by id.

    Args:
        es_id: Primary key.
        db: Injected database session.
    """
    try:
        es = _get_or_404(db, es_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(es)
    db.commit()
    logger.info("Deleted EmployeeSkill id=%d", es_id)
