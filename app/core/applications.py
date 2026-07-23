"""
Application Registry.

Defines the supported applications on Windows with their display names,
executable locations/names, process names, and window name signatures.
"""

from dataclasses import dataclass, field
import os
from typing import Dict, List, Optional


@dataclass
class ApplicationDefinition:
    """
    Metadata registry definition for controlled applications.
    """
    key: str
    display_name: str
    executable_paths: List[str]
    process_names: List[str]
    window_names: List[str]  # partial title matching strings


class ApplicationRegistry:
    """
    Registry for managing application configuration maps.
    """

    def __init__(self) -> None:
        self._apps: Dict[str, ApplicationDefinition] = {}
        self._setup_defaults()

    def register(self, app: ApplicationDefinition) -> None:
        """Register a new application definition."""
        self._apps[app.key.lower()] = app

    def get(self, key: str) -> Optional[ApplicationDefinition]:
        """Retrieve application definition by key."""
        return self._apps.get(key.lower())

    def list_apps(self) -> List[ApplicationDefinition]:
        """Get all registered application definitions."""
        return list(self._apps.values())

    def _setup_defaults(self) -> None:
        # Notepad
        self.register(ApplicationDefinition(
            key="notepad",
            display_name="Notepad",
            executable_paths=["notepad.exe"],
            process_names=["notepad.exe"],
            window_names=["Notepad", "notepad"]
        ))
        
        # Calculator
        self.register(ApplicationDefinition(
            key="calculator",
            display_name="Calculator",
            executable_paths=["calc.exe"],
            process_names=["CalculatorApp.exe", "calc.exe"],
            window_names=["Calculator"]
        ))
        self.register(ApplicationDefinition(
            key="calc",
            display_name="Calculator",
            executable_paths=["calc.exe"],
            process_names=["CalculatorApp.exe", "calc.exe"],
            window_names=["Calculator"]
        ))

        # Paint
        self.register(ApplicationDefinition(
            key="paint",
            display_name="Paint",
            executable_paths=["mspaint.exe"],
            process_names=["mspaint.exe", "PaintDotNet.exe"],
            window_names=["Paint", "mspaint"]
        ))

        # Command Prompt
        self.register(ApplicationDefinition(
            key="cmd",
            display_name="Command Prompt",
            executable_paths=["cmd.exe"],
            process_names=["cmd.exe"],
            window_names=["Command Prompt", "cmd.exe"]
        ))

        # PowerShell
        self.register(ApplicationDefinition(
            key="powershell",
            display_name="PowerShell",
            executable_paths=["powershell.exe"],
            process_names=["powershell.exe"],
            window_names=["PowerShell", "powershell.exe"]
        ))

        # File Explorer
        self.register(ApplicationDefinition(
            key="explorer",
            display_name="File Explorer",
            executable_paths=["explorer.exe"],
            process_names=["explorer.exe"],
            window_names=["File Explorer", "explorer.exe"]
        ))

        # Google Chrome
        self.register(ApplicationDefinition(
            key="chrome",
            display_name="Google Chrome",
            executable_paths=[
                "chrome.exe",
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
            ],
            process_names=["chrome.exe"],
            window_names=["Chrome", "Google Chrome"]
        ))

        # VS Code
        self.register(ApplicationDefinition(
            key="vscode",
            display_name="VS Code",
            executable_paths=[
                "code.cmd",
                "code.exe",
                os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"),
            ],
            process_names=["Code.exe"],
            window_names=["Visual Studio Code", "VS Code", "code"]
        ))


# Instantiate global registry instance
registry = ApplicationRegistry()
