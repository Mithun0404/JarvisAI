"""
Base class for every JARVIS tool.
"""

from abc import ABC, abstractmethod
from app.brain.intent.intents import Intent


class BaseTool(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def intent(self) -> Intent:
        pass

    @abstractmethod
    def execute(self, text: str):
        pass