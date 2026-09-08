"""Decoupled logging via decorators.

Business logic never calls logging directly. Instead, functions are wrapped
with the @logged decorator so logging stays separate from the code that does
the actual work.
"""

import functools
import logging
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)


def logged(func):
    """Log when a function starts and finishes."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger(func.__module__)
        logger.info("start %s", func.__name__)
        try:
            result = func(*args, **kwargs)
        except Exception as exc:
            logger.exception("error in %s: %s", func.__name__, exc)
            raise
        logger.info("done %s", func.__name__)
        return result

    return wrapper