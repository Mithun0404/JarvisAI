"""
Application logging configuration.

Provides a single logger instance for the entire application.
"""

from pathlib import Path

from loguru import logger

from app.core.constants import LOG_DIR, LOG_FILE


def setup_logger():
    """
    Configure console and file logging.
    """

    # Create log directory if it doesn't exist
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

    # Remove default logger
    logger.remove()

    # Console Logger
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level="INFO",
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>"
    )

    # File Logger
    logger.add(
        LOG_FILE,
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        level="DEBUG",
        encoding="utf-8",
        format="{time:YYYY-MM-DD HH:mm:ss} | "
               "{level:<8} | "
               "{name}:{function}:{line} - "
               "{message}"
    )

    logger.success("Logger initialized successfully.")


# Global logger object
log = logger