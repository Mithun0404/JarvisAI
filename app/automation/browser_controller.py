"""
Browser Controller Module.

Provides reusable browser control primitives.
"""

from urllib.parse import quote
import webbrowser

from app.automation.keyboard import KeyboardController
from app.automation.mouse import MouseController


class BrowserController:
    """
    Handles higher level web automation capabilities.
    """

    def __init__(self) -> None:
        self.keyboard = KeyboardController()
        self.mouse = MouseController()

    def open_url(self, url: str) -> str:
        """
        Opens a specified URL in the default browser.
        """
        webbrowser.open(url)
        return f"Opened URL: '{url}'"

    def search(self, query: str) -> str:
        """
        Performs a Google Search in the default web browser.
        """
        encoded_query = quote(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        return self.open_url(url)

    def scroll(self, direction: str = "down", amount: int = 3) -> str:
        """
        Scrolls the screen using standard keyboard page events or mouse scrolls.
        """
        direction = direction.lower()
        if direction == "down":
            for _ in range(amount):
                self.keyboard.press("pagedown")
            return f"Scrolled browser down by {amount} keyboard pages."
        elif direction == "up":
            for _ in range(amount):
                self.keyboard.press("pageup")
            return f"Scrolled browser up by {amount} keyboard pages."
        else:
            return f"Unsupported scroll direction: '{direction}'."

    def new_tab(self) -> str:
        """
        Opens a new tab in the active browser using Ctrl+T.
        """
        self.keyboard.hotkey("ctrl", "t")
        return "Opened new browser tab."

    def close_tab(self) -> str:
        """
        Closes the active browser tab using Ctrl+W.
        """
        self.keyboard.hotkey("ctrl", "w")
        return "Closed active browser tab."

    def go_back(self) -> str:
        """
        Navigates back in history (Alt + Left).
        """
        self.keyboard.hotkey("alt", "left")
        return "Navigated back in browser history."

    def go_forward(self) -> str:
        """
        Navigates forward in history (Alt + Right).
        """
        self.keyboard.hotkey("alt", "right")
        return "Navigated forward in browser history."
