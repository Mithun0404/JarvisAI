"""
Automation controller.
"""

from app.automation.mouse import MouseController
from app.automation.keyboard import KeyboardController
from app.automation.clipboard import ClipboardController


class AutomationController:

    def __init__(self):

        self.mouse = MouseController()

        self.keyboard = KeyboardController()

        self.clipboard = ClipboardController()