import logging
import sys
from typing import Optional

_CONFIGURED = False


def setup_logging(level: Optional[str] = None) -> None:
    """Configure application-wide structured logging."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    log_level = getattr(logging, (level or "INFO").upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a named logger instance, initializing logging if needed."""
    if not _CONFIGURED:
        setup_logging()
    return logging.getLogger(name)
