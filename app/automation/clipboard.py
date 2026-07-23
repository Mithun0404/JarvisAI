"""
Clipboard automation.
"""

from typing import Optional
import win32clipboard


class ClipboardController:
    """
    Handles reading and writing to the Windows OS clipboard.
    """

    def set_text(self, text: str) -> bool:
        """
        Sets text content to the clipboard.
        """
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            return True
        except Exception:
            return False

    def get_text(self) -> str:
        """
        Retrieves text from the clipboard.
        """
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
            if isinstance(data, str):
                return data
            return ""
        except Exception:
            return ""
