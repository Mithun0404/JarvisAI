"""
Base AI provider.
"""

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """
    Base class for every AI provider.
    """

    @abstractmethod
    def chat(self, messages: list[dict], json_mode: bool = False) -> str:
        """
        Generate a response.
        """
        pass