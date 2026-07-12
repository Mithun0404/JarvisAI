"""
Base AI provider.
"""

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """
    Base class for every AI provider.
    """

    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        """
        Generate a response.
        """
        pass