"""
Tool manager.
"""

from app.tools.application_tool import ApplicationTool


class ToolManager:

    def __init__(self):

        self.tools = {}

        self.register(ApplicationTool())

    def register(self, tool):

        self.tools[tool.intent] = tool

    def execute(self, intent, argument):

        tool = self.tools.get(intent)

        if tool is None:
            return "No tool available."

        return tool.execute(argument)

    def list_tools(self):

        return [tool.name for tool in self.tools.values()]