"""
Command router for JARVIS.
"""

from app.core.logger import log


class CommandRouter:
    """
    Registers and executes commands.
    """

    def __init__(self):
        self._commands = {}

    def register(self, command: str, handler):
        """
        Register a new command.
        """

        command = command.lower()

        if command in self._commands:
            raise ValueError(f"'{command}' is already registered.")

        self._commands[command] = handler

    def execute(self, command: str):
        """
        Execute a command.
        """

        command = command.lower()

        if command not in self._commands:
            log.warning("Unknown command: {}", command)
            return

        self._commands[command]()

    def list_commands(self):
        """
        Return all registered commands.
        """

        return sorted(self._commands.keys())