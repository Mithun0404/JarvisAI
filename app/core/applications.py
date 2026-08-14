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
        """Retrieve application definition by key with fuzzy key and display name matching."""
        clean_key = key.lower().strip().replace(" ", "")
        
        # 1. Exact key match
        if clean_key in self._apps:
            return self._apps[clean_key]

        # 2. Key mapping aliases
        aliases = {
            "microsoftedge": "edge",
            "msedge": "edge",
            "googlechrome": "chrome",
            "microsoftword": "word",
            "msword": "word",
            "microsoftexcel": "excel",
            "msexcel": "excel",
            "microsoftpowerpoint": "powerpoint",
            "powerpnt": "powerpoint",
            "windowsterminal": "terminal",
            "wt": "terminal",
            "controlpanel": "control",
        }
        if clean_key in aliases and aliases[clean_key] in self._apps:
            return self._apps[aliases[clean_key]]

        # 3. Partial substring matching against keys or display names
        for app in self._apps.values():
            if clean_key in app.key.lower().replace(" ", "") or clean_key in app.display_name.lower().replace(" ", ""):
                return app

        return None

    def list_apps(self) -> List[ApplicationDefinition]:
        """Get all registered application definitions, deduplicated (aliases share the same definition)."""
        seen_ids = set()
        unique_apps = []
        for app in self._apps.values():
            if id(app) not in seen_ids:
                seen_ids.add(id(app))
                unique_apps.append(app)
        return unique_apps

    def _setup_defaults(self) -> None:
        # Microsoft Edge
        edge_def = ApplicationDefinition(
            key="edge",
            display_name="Microsoft Edge",
            executable_paths=[
                "msedge.exe",
                "msedge",
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            ],
            process_names=["msedge.exe"],
            window_names=["Edge", "Microsoft Edge"]
        )
        self.register(edge_def)
        self._apps["microsoft edge"] = edge_def
        self._apps["msedge"] = edge_def

        # Notepad
        self.register(ApplicationDefinition(
            key="notepad",
            display_name="Notepad",
            executable_paths=["notepad.exe"],
            process_names=["notepad.exe"],
            window_names=["Notepad", "notepad"]
        ))
        
        # Calculator
        calc_def = ApplicationDefinition(
            key="calculator",
            display_name="Calculator",
            executable_paths=["calc.exe"],
            process_names=["CalculatorApp.exe", "calc.exe"],
            window_names=["Calculator"]
        )
        self.register(calc_def)
        self._apps["calc"] = calc_def

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
        chrome_def = ApplicationDefinition(
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
        )
        self.register(chrome_def)
        self._apps["google chrome"] = chrome_def

        # Firefox
        self.register(ApplicationDefinition(
            key="firefox",
            display_name="Firefox",
            executable_paths=[
                "firefox.exe",
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            ],
            process_names=["firefox.exe"],
            window_names=["Firefox", "Mozilla Firefox"]
        ))

        # Brave
        self.register(ApplicationDefinition(
            key="brave",
            display_name="Brave Browser",
            executable_paths=[
                "brave.exe",
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            ],
            process_names=["brave.exe"],
            window_names=["Brave"]
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

        # Microsoft Word
        self.register(ApplicationDefinition(
            key="word",
            display_name="Microsoft Word",
            executable_paths=["WINWORD.EXE", "winword.exe"],
            process_names=["WINWORD.EXE"],
            window_names=["Word"]
        ))

        # Microsoft Excel
        self.register(ApplicationDefinition(
            key="excel",
            display_name="Microsoft Excel",
            executable_paths=["EXCEL.EXE", "excel.exe"],
            process_names=["EXCEL.EXE"],
            window_names=["Excel"]
        ))

        # Microsoft PowerPoint
        self.register(ApplicationDefinition(
            key="powerpoint",
            display_name="Microsoft PowerPoint",
            executable_paths=["POWERPNT.EXE", "powerpnt.exe"],
            process_names=["POWERPNT.EXE"],
            window_names=["PowerPoint"]
        ))

        # Spotify
        self.register(ApplicationDefinition(
            key="spotify",
            display_name="Spotify",
            executable_paths=[
                "spotify.exe",
                os.path.expandvars(r"%APPDATA%\Spotify\Spotify.exe"),
            ],
            process_names=["Spotify.exe"],
            window_names=["Spotify"]
        ))

        # Windows Terminal
        self.register(ApplicationDefinition(
            key="terminal",
            display_name="Windows Terminal",
            executable_paths=["wt.exe", "WindowsTerminal.exe"],
            process_names=["WindowsTerminal.exe", "wt.exe"],
            window_names=["Terminal", "Windows Terminal"]
        ))


# Instantiate global registry instance
registry = ApplicationRegistry()
