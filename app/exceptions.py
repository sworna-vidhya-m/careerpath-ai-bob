"""Domain exception hierarchy for CareerPath AI Bob.

Routers catch these and translate them to appropriate HTTPException responses:
  NotFoundError   -> 404
  DuplicateError  -> 409
  ValidationError -> 422
  BusinessRuleError -> 400
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception for all application-level errors.

    Args:
        message: Human-readable description of the error.
        details: Optional dict with additional context.
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotFoundError(AppException):
    """Raised when a requested resource does not exist."""


class DuplicateError(AppException):
    """Raised when a create operation would violate a unique constraint."""


class ValidationError(AppException):
    """Raised when input fails domain-level validation beyond schema checks."""


class BusinessRuleError(AppException):
    """Raised when an operation violates a business rule."""


def raise_http_from_app_exception(exc: AppException) -> None:
    """Translate a domain exception into the appropriate HTTPException.

    Args:
        exc: A domain-level AppException subclass.

    Raises:
        fastapi.HTTPException: Always raised with an appropriate status code.
    """
    from fastapi import HTTPException

    status_map = {
        NotFoundError: 404,
        DuplicateError: 409,
        ValidationError: 422,
        BusinessRuleError: 400,
    }
    status_code = status_map.get(type(exc), 500)
    raise HTTPException(status_code=status_code, detail={"message": exc.message, **exc.details})
