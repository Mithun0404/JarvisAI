"""
Demo tool.
"""

from app.tools.base import BaseTool


class EchoTool(BaseTool):

    @property
    def name(self):

        return "echo"

    def execute(self, text):

        return f"Echo Tool: {text}"