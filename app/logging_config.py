"""Logging configuration for the CareerPath AI Bob application.

Provides a single configure_logging() function that sets up structured
stdout logging for the entire application. Called once at startup.
"""

import logging
import sys

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
DEFAULT_LEVEL = logging.INFO

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure root logger with stdout handler and standard format.

    Sets INFO level on the root logger and attaches a StreamHandler that
    writes to stdout. Idempotent — safe to call multiple times.
    """
    root_logger = logging.getLogger()
    if root_logger.handlers:
        # Already configured — avoid duplicate handlers.
        return

    root_logger.setLevel(DEFAULT_LEVEL)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(DEFAULT_LEVEL)
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    logger.info("Logging configured at INFO level.")
