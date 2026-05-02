"""Employees router providing CRUD endpoints with filtering for Employee entities."""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import DuplicateError, NotFoundError, raise_http_from_app_exception
from app.models import Employee, EmployeeStatus
from app.schemas import EmployeeCreate, EmployeeRead, EmployeeUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/employees", tags=["employees"])

MAX_LIMIT = 500


def _get_or_404(db: Session, emp_id: int) -> Employee:
    """Retrieve an Employee by id or raise NotFoundError.

    Args:
        db: Active database session.
        emp_id: Primary key.

    Returns:
        The matching Employee ORM instance.
    """
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise NotFoundError(f"Employee {emp_id} not found.")
    return emp


@router.get("/", response_model=List[EmployeeRead])
def list_employees(
    skip: int = 0,
    limit: int = 100,
    business_unit_id: Optional[int] = Query(None),
    status: Optional[EmployeeStatus] = Query(None),
    band: Optional[str] = Query(None),
    db: Session = Depends(get_db),
) -> List[Employee]:
    """Return a paginated, filtered list of employees.

    Args:
        skip: Offset for pagination.
        limit: Max results (capped at 500).
        business_unit_id: Filter by business unit.
        status: Filter by EmployeeStatus enum value.
        band: Filter by band string.
        db: Injected database session.
    """
    limit = min(limit, MAX_LIMIT)
    query = db.query(Employee)
    if business_unit_id is not None:
        query = query.filter(Employee.business_unit_id == business_unit_id)
    if status is not None:
        query = query.filter(Employee.current_status == status)
    if band is not None:
        query = query.filter(Employee.band == band)
    return query.offset(skip).limit(limit).all()


@router.get("/{emp_id}", response_model=EmployeeRead)
def get_employee(emp_id: int, db: Session = Depends(get_db)) -> Employee:
    """Retrieve a single employee by id.

    Args:
        emp_id: Primary key.
        db: Injected database session.
    """
    try:
        return _get_or_404(db, emp_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)


@router.post("/", response_model=EmployeeRead, status_code=201)
def create_employee(payload: EmployeeCreate, db: Session = Depends(get_db)) -> Employee:
    """Create a new employee record.

    Args:
        payload: Validated creation payload.
        db: Injected database session.

    Raises:
        HTTPException 409: If the email address is already in use.
    """
    emp = Employee(**payload.model_dump())
    db.add(emp)
    try:
        db.commit()
        db.refresh(emp)
        logger.info("Created Employee id=%d email=%s", emp.id, emp.email)
        return emp
    except IntegrityError:
        db.rollback()
        raise_http_from_app_exception(DuplicateError(f"Email '{payload.email}' already in use."))


@router.put("/{emp_id}", response_model=EmployeeRead)
def update_employee(
    emp_id: int, payload: EmployeeUpdate, db: Session = Depends(get_db)
) -> Employee:
    """Update an existing employee (partial update supported).

    Args:
        emp_id: Primary key of the employee to update.
        payload: Fields to update.
        db: Injected database session.
    """
    try:
        emp = _get_or_404(db, emp_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(emp, field, value)
    try:
        db.commit()
        db.refresh(emp)
        logger.info("Updated Employee id=%d", emp_id)
        return emp
    except IntegrityError:
        db.rollback()
        raise_http_from_app_exception(DuplicateError("Email already in use."))


@router.delete("/{emp_id}", status_code=204)
def delete_employee(emp_id: int, db: Session = Depends(get_db)) -> None:
    """Delete an employee by id.

    Args:
        emp_id: Primary key of the employee to delete.
        db: Injected database session.
    """
    try:
        emp = _get_or_404(db, emp_id)
    except NotFoundError as exc:
        raise_http_from_app_exception(exc)

    db.delete(emp)
    db.commit()
    logger.info("Deleted Employee id=%d", emp_id)
