"""
Application launcher tool.
"""

import os
import shutil
import subprocess

from app.tools.base import BaseTool


class ApplicationTool(BaseTool):

    @property
    def name(self):
        return "application"

    @property
    def intent(self):
        return "OPEN_APPLICATION"

    def execute(self, application):

        application = application.lower()

        apps = {
            "notepad": ["notepad.exe"],
            "calculator": ["calc.exe"],
            "calc": ["calc.exe"],
            "paint": ["mspaint.exe"],
            "cmd": ["cmd.exe"],
            "powershell": ["powershell.exe"],
            "explorer": ["explorer.exe"],

            "chrome": [
                "chrome.exe",
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expandvars(
                    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
                ),
            ],

            "vscode": [
                "code.cmd",
                os.path.expandvars(
                    r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
                ),
            ],
        }

        if application not in apps:
            return f"{application} is not supported."

        for executable in apps[application]:

            path = shutil.which(executable)

            if path:
                subprocess.Popen([path])
                return f"Opening {application}..."

            if os.path.exists(executable):
                subprocess.Popen([executable])
                return f"Opening {application}..."

        return f"Could not find {application} on this computer."