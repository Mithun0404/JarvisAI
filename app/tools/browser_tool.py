"""
Browser automation tool.
"""

import webbrowser
from urllib.parse import quote

from app.tools.base import BaseTool


class BrowserTool(BaseTool):

    @property
    def name(self):
        return "browser"

    @property
    def intent(self):
        return "WEB_AUTOMATION"

    def execute(self, data):

        print("BrowserTool.execute() called")
        print("Received:", data)

        if not isinstance(data, dict):
            return f"Expected dict, got {type(data)}"

        action = str(data.get("action", "")).upper()
        query = data.get("query", "")

        if action == "SEARCH":

            url = f"https://www.google.com/search?q={quote(query)}"

            webbrowser.open(url)

            return f'Searching Google for "{query}"...'

        return f"Unsupported web action: {action}"