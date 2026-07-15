"""
Browser search tool.
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
        return "SEARCH_WEB"

    def execute(self, query):

        url = f"https://www.google.com/search?q={quote(query)}"

        webbrowser.open(url)

        return f'Searching Google for "{query}"...'