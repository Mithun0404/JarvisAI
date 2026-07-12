"""
Startup manager for JARVIS.

Responsible for initializing all core services
before the application starts.
"""

from core.registry import registry
from core.constants import BANNER
from core.config import settings
from core.logger import setup_logger, log
from core.events import event_bus


def startup():
    """
    Initialize the JARVIS application.
    """

    # Print application banner
    print(BANNER)

    # Initialize logging
    setup_logger()

    # Application information
    log.info("Application Name : {}", settings.app_name)
    log.info("Version          : {}", settings.version)
    log.info("Author           : {}", settings.author)
    log.info("Environment      : {}", settings.environment)
    log.info("Debug Mode       : {}", settings.debug)
    log.info("Log Level        : {}", settings.log_level)

    log.success("JARVIS initialized successfully.")
    registry.register("config", settings)
    registry.register("logger", log)

    log.success("Core services registered.")
    registry.register("event_bus", event_bus)