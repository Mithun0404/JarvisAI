"""
Application launcher tool.
"""

import os
import shutil
import subprocess

from app.tools.base import BaseTool


from app.automation.app_manager import ApplicationManager


class ApplicationTool(BaseTool):

    def __init__(self):
        self.app_manager = ApplicationManager()

    @property
    def name(self):
        return "application"

    @property
    def intent(self):
        return "OPEN_APPLICATION"

    def execute(self, application):
        if isinstance(application, dict):
            application = application.get("application", "")

        app_name = str(application).strip()
        return self.app_manager.start_application(app_name)