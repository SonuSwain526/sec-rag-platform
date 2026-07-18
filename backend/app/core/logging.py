"""
Logging Configuration Module for sec-rag.

This module initializes and configures logging parameters for FastAPI,
providing standard formatting, console handlers, and log level resolution.
"""

import logging
import sys
from typing import Any, Dict


def setup_app_logging() -> None:
    """
    Sets up application-wide logger layout and handler configuration.
    
    TODO: Support file logging and integration with external monitoring systems (e.g., Sentry).
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Disable verbose logging from third party libraries
    # TODO: Add configurable overrides for development/debugging
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance for the given module name.
    
    Args:
        name: The module or component name.
        
    Returns:
        A logger instance.
    """
    # TODO: Wrap this with custom logging utility to add contextual span info (e.g. tracing)
    return logging.getLogger(name)
