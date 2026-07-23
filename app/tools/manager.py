"""
Tool manager.
"""

from json import tool

from click import argument

from app.tools.application_tool import ApplicationTool
from app.tools.browser_tool import BrowserTool
from app.tools.automation_tool import AutomationTool
from app.tools.close_application_tool import CloseApplicationTool


class ToolManager:

    def __init__(self):

        self.tools = {}

        self.register(ApplicationTool())

        self.register(BrowserTool())

        self.register(AutomationTool())

        self.register(CloseApplicationTool())

    def register(self, tool):

        self.tools[tool.intent] = tool

    def execute(self, intent, argument):

        print("Intent:", intent)
        print("Argument:", argument)

        tool = self.tools.get(intent)

        print("Tool:", tool)

        if tool is None:
            return "No tool available."

        return tool.execute(argument)

    def list_tools(self):

        return [tool.name for tool in self.tools.values()]