import logging
import sys

from app.core.config import get_settings

settings = get_settings()


def setup_logging() -> None:
    """
    Configures application-wide structured logging.
    In production, you'd swap this for JSON-formatted logs
    (e.g., via `python-json-logger`) for log aggregation tools —
    plain text is fine for a portfolio project running locally.
    """
    level = logging.DEBUG if settings.DEBUG else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Quiet down noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)