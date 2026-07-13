"""
Intent definitions for JARVIS.
"""

from enum import Enum


class Intent(Enum):

    OPEN_APPLICATION = "open_application"

    GENERAL_CHAT = "general_chat"

    UNKNOWN = "unknown"