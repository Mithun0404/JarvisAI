"""
Application-wide constants.

This module contains values that are used throughout the project.
Avoid hardcoding strings or paths in other modules.
"""

from pathlib import Path

# -------------------------------------------------------------------
# Application Information
# -------------------------------------------------------------------

APP_NAME = "JARVIS"
VERSION = "0.1.0"
AUTHOR = "Mithun Y"

# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

APP_DIR = PROJECT_ROOT / "app"
DATA_DIR = PROJECT_ROOT / "data"
LOG_DIR = PROJECT_ROOT / "logs"
MODELS_DIR = PROJECT_ROOT / "models"
RESOURCES_DIR = PROJECT_ROOT / "resources"
DOCS_DIR = PROJECT_ROOT / "docs"

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------

LOG_FILE = LOG_DIR / "jarvis.log"

# -------------------------------------------------------------------
# Startup Banner
# -------------------------------------------------------------------

BANNER = rf"""
==================================================
                 {APP_NAME} v{VERSION}
==================================================
      Just A Rather Very Intelligent System
==================================================
"""

# -------------------------------------------------------------------
# Exit Codes
# -------------------------------------------------------------------

SUCCESS = 0
ERROR = 1

# -------------------------------------------------------------------
# Environment
# -------------------------------------------------------------------

ENV_DEV = "development"
ENV_PROD = "production"
DEFAULT_ENV = ENV_DEV

# -------------------------------------------------------------------
# Application Settings
# -------------------------------------------------------------------

DEFAULT_LANGUAGE = "en"
DEFAULT_THEME = "dark"
DEFAULT_LOG_LEVEL = "INFO"

# -------------------------------------------------------------------
# Startup
# -------------------------------------------------------------------

WELCOME_MESSAGE = "Welcome back. Systems are online."