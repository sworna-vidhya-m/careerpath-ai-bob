"""Skills router providing CRUD endpoints for Skill entities."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import DuplicateError, NotFoundError, raise_http_from_app_exception
from app.models import Skill, SkillCategory
from app.schemas import SkillCreate, SkillRead, SkillUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/skills", tags=["skills"])

MAX_LIMIT = 500


def _get_or_404(db: Session, skill_id: int) -> Skill:
    """Retrieve a Skill by id or raise NotFoundError.

    Args:
        db: Active database session.
        skill_id: Primary key.
    """
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise NotFoundError(f"Skill {skill_id} not found.")
    return skill


@router.get("/", response_model=List[SkillRead])
def list_skills(
    skip: int = 0,
    limit: int = 100,
    category: Optional[SkillCategory] = Query(None),
    is_emerging: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
) -> List[Skill]:
    """Return a paginated list of skills with optional filters.

    Args:
        skip: Offset for pagination.
        limit: Maximum results (capped at 500).
        category: Filter by skill category.
        is_emerging: Filter by emerging flag.
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    query = db.query(Skill)
    if category is not None:
        query = query.filter(Skill.category == category)
    if is_emerging is not None:
        query = query.filter(Skill.is_emerging == is_emerging)
    return query.offset(skip).limit(limit).all()


@router.get("/{skill_id}", response_model=SkillRead)
def get_skill(skill_id: int, db: Session = Depends(get_db)) -> Skill:
    """Retrieve a single skill by id.

    Args:
        skill_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, skill_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=SkillRead, status_code=201)
def create_skill(payload: SkillCreate, db: Session = Depends(get_db)) -> Skill:
    """Create a new skill.

    Args:
        payload: Validated creation payload.
        db: Injected database session.

    Raises:
        HTTPException 409: If a skill with the same name already exists.
    """
    skill = Skill(**payload.model_dump())
    db.add(skill)
    try:
        db.commit()
        db.refresh(skill)
        logger.info("Created Skill id=%d name=%s", skill.id, skill.name)
        return skill
    except IntegrityError:
        db.rollback()
        raise_http_from_app_exception(DuplicateError(f"Skill '{payload.name}' already exists."))


@router.put("/{skill_id}", response_model=SkillRead)
def update_skill(
    skill_id: int, payload: SkillUpdate, db: Session = Depends(get_db)
) -> Skill:
    """Update an existing skill (partial update supported).

    Args:
        skill_id: Primary key.
        payload: Fields to update.
        db: Injected database session.
    """
    try:
        skill = _get_or_404(db, skill_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(skill, field, value)
    try:
        db.commit()
        db.refresh(skill)
        logger.info("Updated Skill id=%d", skill_id)
        return skill
    except IntegrityError:
        db.rollback()
        raise_http_from_app_exception(DuplicateError("Skill name already in use."))


@router.delete("/{skill_id}", status_code=204)
def delete_skill(skill_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a skill by id.

    Args:
        skill_id: Primary key.
        db: Injected database session.
    """
    try:
        skill = _get_or_404(db, skill_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(skill)
    db.commit()
    logger.info("Deleted Skill id=%d", skill_id)
