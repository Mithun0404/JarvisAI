"""
Mouse automation.
"""

from typing import Tuple
import pyautogui


class MouseController:

    def move(self, x: int, y: int) -> str:
        pyautogui.moveTo(x, y, duration=0.3)
        return f"Mouse moved to ({x}, {y})."

    def click(self) -> str:
        pyautogui.click()
        return "Mouse clicked."

    def double_click(self) -> str:
        pyautogui.doubleClick()
        return "Mouse double-clicked."

    def right_click(self) -> str:
        pyautogui.rightClick()
        return "Mouse right-clicked."
        
    def drag_to(self, x: int, y: int) -> str:
        pyautogui.dragTo(x, y, duration=0.5)
        return f"Mouse dragged to ({x}, {y})."

    def press(self) -> str:
        pyautogui.mouseDown()
        return "Mouse button pressed down."

    def release(self) -> str:
        pyautogui.mouseUp()
        return "Mouse button released."

    def get_position(self) -> Tuple[int, int]:
        return pyautogui.position()

    def scroll(self, amount: int) -> str:
        pyautogui.scroll(amount)
        return f"Scrolled click-steps: {amount}."