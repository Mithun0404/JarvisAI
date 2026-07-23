"""
Close application tool.
"""

import subprocess

from app.tools.base import BaseTool


class CloseApplicationTool(BaseTool):

    @property
    def name(self):
        return "close_application"

    @property
    def intent(self):
        return "CLOSE_WINDOW"

    def execute(self, application):

        if isinstance(application, dict):
            application = application.get("application", "")

        application = application.lower()

        apps = {
            "chrome": "chrome.exe",
            "notepad": "notepad.exe",
            "paint": "mspaint.exe",
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
            "explorer": "explorer.exe",
            "vscode": "Code.exe",
        }

        exe = apps.get(application)

        if exe is None:
            return f"{application} is not supported."

        result = subprocess.run(
            ["taskkill", "/F", "/IM", exe],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return f"Closed {application}."

        return result.stderr.strip()