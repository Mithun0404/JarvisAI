"""
Service registry for JARVIS.

Stores references to shared services and modules.
"""

from typing import Any


class ServiceRegistry:
    """
    Registry for application services.
    """

    def __init__(self):
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """
        Register a service.
        """
        if name in self._services:
            raise ValueError(f"Service '{name}' is already registered.")

        self._services[name] = service

    def get(self, name: str) -> Any:
        """
        Get a registered service.
        """
        if name not in self._services:
            raise KeyError(f"Service '{name}' is not registered.")

        return self._services[name]

    def exists(self, name: str) -> bool:
        """
        Check whether a service exists.
        """
        return name in self._services

    def list_services(self) -> list[str]:
        """
        Return all registered service names.
        """
        return list(self._services.keys())


registry = ServiceRegistry()