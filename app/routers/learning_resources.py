"""Learning Resources router providing CRUD endpoints for LearningResource entities."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import NotFoundError, raise_http_from_app_exception
from app.models import LearningResource, LearningResourceType
from app.schemas import LearningResourceCreate, LearningResourceRead, LearningResourceUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/learning-resources", tags=["learning-resources"])

MAX_LIMIT = 500


def _get_or_404(db: Session, resource_id: int) -> LearningResource:
    """Retrieve a LearningResource by id or raise NotFoundError.

    Args:
        db: Active database session.
        resource_id: Primary key.
    """
    resource = db.query(LearningResource).filter(LearningResource.id == resource_id).first()
    if not resource:
        raise NotFoundError(f"LearningResource {resource_id} not found.")
    return resource


@router.get("/", response_model=List[LearningResourceRead])
def list_learning_resources(
    skip: int = 0,
    limit: int = 100,
    skill_id: Optional[int] = Query(None),
    resource_type: Optional[LearningResourceType] = Query(None),
    db: Session = Depends(get_db),
) -> List[LearningResource]:
    """Return a paginated list of learning resources with optional filters.

    Args:
        skip: Offset for pagination.
        limit: Maximum results (capped at 500).
        skill_id: Filter by associated skill.
        resource_type: Filter by resource type.
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    query = db.query(LearningResource)
    if skill_id is not None:
        query = query.filter(LearningResource.skill_id == skill_id)
    if resource_type is not None:
        query = query.filter(LearningResource.type == resource_type)
    return query.offset(skip).limit(limit).all()


@router.get("/{resource_id}", response_model=LearningResourceRead)
def get_learning_resource(resource_id: int, db: Session = Depends(get_db)) -> LearningResource:
    """Retrieve a single learning resource by id.

    Args:
        resource_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, resource_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=LearningResourceRead, status_code=201)
def create_learning_resource(
    payload: LearningResourceCreate, db: Session = Depends(get_db)
) -> LearningResource:
    """Create a new learning resource.

    Args:
        payload: Validated creation payload.
        db: Injected database session.
    """
    resource = LearningResource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    logger.info("Created LearningResource id=%d title=%s", resource.id, resource.title)
    return resource


@router.put("/{resource_id}", response_model=LearningResourceRead)
def update_learning_resource(
    resource_id: int, payload: LearningResourceUpdate, db: Session = Depends(get_db)
) -> LearningResource:
    """Update an existing learning resource (partial update supported).

    Args:
        resource_id: Primary key.
        payload: Fields to update.
        db: Injected database session.
    """
    try:
        resource = _get_or_404(db, resource_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    db.commit()
    db.refresh(resource)
    logger.info("Updated LearningResource id=%d", resource_id)
    return resource


@router.delete("/{resource_id}", status_code=204)
def delete_learning_resource(resource_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a learning resource by id.

    Args:
        resource_id: Primary key.
        db: Injected database session.
    """
    try:
        resource = _get_or_404(db, resource_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(resource)
    db.commit()
    logger.info("Deleted LearningResource id=%d", resource_id)
