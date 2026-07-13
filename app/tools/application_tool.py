"""
Application launcher tool.
"""

import subprocess

from app.brain.intent.intents import Intent
from app.tools.base import BaseTool


class ApplicationTool(BaseTool):

    @property
    def name(self):
        return "application"

    @property
    def intent(self):
        return Intent.OPEN_APPLICATION

    def execute(self, application):

        apps = {

            "notepad": "notepad",
            "calc": "calc",
            "calculator": "calc",
            "paint": "mspaint",
            "cmd": "cmd",
            "powershell": "powershell",
            "explorer": "explorer",
            "chrome": "chrome",
            "vscode": "code",

        }

        app = apps.get(application.lower())

        if app is None:
            return f"{application} is not supported."

        subprocess.Popen(app)

        return f"Opening {application}..."