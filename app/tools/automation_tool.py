"""
Desktop automation tool.
"""

from app.automation.controller import AutomationController
from app.tools.base import BaseTool


class AutomationTool(BaseTool):

    def __init__(self):

        self.controller = AutomationController()

    @property
    def name(self):
        return "automation"

    @property
    def intent(self):
        return "DESKTOP_AUTOMATION"

    def execute(self, command: dict):
        
        print(command)

        action = command.get("action")

        if action == "move":

            return self.controller.mouse.move(
                command["x"],
                command["y"],
            )

        elif action == "click":

            return self.controller.mouse.click()

        elif action == "double_click":

            return self.controller.mouse.double_click()

        elif action == "right_click":

            return self.controller.mouse.right_click()

        elif action == "type":

            return self.controller.keyboard.type_text(
                command["text"]
            )

        elif action == "press":

            return self.controller.keyboard.press(
                command["key"]
            )

        return "Unknown automation action."