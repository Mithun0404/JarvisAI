"""
Keyboard automation.
"""

from typing import List
import pyautogui


class KeyboardController:

    def type_text(self, text: str, interval: float = 0.01) -> str:
        """Types the specified text on the keyboard."""
        pyautogui.write(text, interval=interval)
        return f"Typed text: '{text}'."

    def press(self, key: str) -> str:
        """Presses and releases a single key."""
        pyautogui.press(key)
        return f"Pressed key: '{key}'."

    def hotkey(self, *keys: str) -> str:
        """Triggers a keyboard shortcut (sequence of keys pressed and released)."""
        pyautogui.hotkey(*keys)
        return f"Triggered shortcut: {'+'.join(keys)}."

    def key_down(self, key: str) -> str:
        """Holds a key down."""
        pyautogui.keyDown(key)
        return f"Held key down: '{key}'."

    def key_up(self, key: str) -> str:
        """Releases a held key."""
        pyautogui.keyUp(key)
        return f"Released key: '{key}'."