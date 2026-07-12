"""
Simple event bus for JARVIS.
"""

from collections import defaultdict
from typing import Callable, Any


class EventBus:
    """
    Handles publish/subscribe communication.
    """

    def __init__(self):
        self._listeners = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """
        Register a listener for an event.
        """
        self._listeners[event_name].append(callback)

    def emit(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        """
        Trigger an event.
        """
        for callback in self._listeners[event_name]:
            callback(*args, **kwargs)


event_bus = EventBus()