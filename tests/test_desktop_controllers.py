"""
Unit tests for unified desktop control controllers (Mouse, Keyboard, Clipboard).
"""

import unittest
from unittest.mock import patch, MagicMock

from app.automation.mouse import MouseController
from app.automation.keyboard import KeyboardController
from app.automation.clipboard import ClipboardController


class TestMouseController(unittest.TestCase):

    def setUp(self):
        self.mouse = MouseController()

    @patch("pyautogui.moveTo")
    def test_move(self, mock_move):
        result = self.mouse.move(100, 200)
        self.assertEqual(result, "Mouse moved to (100, 200).")
        mock_move.assert_called_once_with(100, 200, duration=0.3)

    @patch("pyautogui.click")
    def test_click(self, mock_click):
        result = self.mouse.click()
        self.assertEqual(result, "Mouse clicked.")
        mock_click.assert_called_once()

    @patch("pyautogui.doubleClick")
    def test_double_click(self, mock_dblclick):
        result = self.mouse.double_click()
        self.assertEqual(result, "Mouse double-clicked.")
        mock_dblclick.assert_called_once()

    @patch("pyautogui.rightClick")
    def test_right_click(self, mock_rclick):
        result = self.mouse.right_click()
        self.assertEqual(result, "Mouse right-clicked.")
        mock_rclick.assert_called_once()

    @patch("pyautogui.dragTo")
    def test_drag_to(self, mock_drag):
        result = self.mouse.drag_to(300, 400)
        self.assertEqual(result, "Mouse dragged to (300, 400).")
        mock_drag.assert_called_once_with(300, 400, duration=0.5)

    @patch("pyautogui.mouseDown")
    def test_press(self, mock_down):
        result = self.mouse.press()
        self.assertEqual(result, "Mouse button pressed down.")
        mock_down.assert_called_once()

    @patch("pyautogui.mouseUp")
    def test_release(self, mock_up):
        result = self.mouse.release()
        self.assertEqual(result, "Mouse button released.")
        mock_up.assert_called_once()

    @patch("pyautogui.position")
    def test_get_position(self, mock_pos):
        mock_pos.return_value = (50, 60)
        self.assertEqual(self.mouse.get_position(), (50, 60))

    @patch("pyautogui.scroll")
    def test_scroll(self, mock_scroll):
        result = self.mouse.scroll(10)
        self.assertEqual(result, "Scrolled click-steps: 10.")
        mock_scroll.assert_called_once_with(10)


class TestKeyboardController(unittest.TestCase):

    def setUp(self):
        self.keyboard = KeyboardController()

    @patch("pyautogui.write")
    def test_type_text(self, mock_write):
        result = self.keyboard.type_text("Hello")
        self.assertEqual(result, "Typed text: 'Hello'.")
        mock_write.assert_called_once_with("Hello", interval=0.01)

    @patch("pyautogui.press")
    def test_press(self, mock_press):
        result = self.keyboard.press("enter")
        self.assertEqual(result, "Pressed key: 'enter'.")
        mock_press.assert_called_once_with("enter")

    @patch("pyautogui.hotkey")
    def test_hotkey(self, mock_hotkey):
        result = self.keyboard.hotkey("ctrl", "c")
        self.assertEqual(result, "Triggered shortcut: ctrl+c.")
        mock_hotkey.assert_called_once_with("ctrl", "c")

    @patch("pyautogui.keyDown")
    def test_key_down(self, mock_keydown):
        result = self.keyboard.key_down("shift")
        self.assertEqual(result, "Held key down: 'shift'.")
        mock_keydown.assert_called_once_with("shift")

    @patch("pyautogui.keyUp")
    def test_key_up(self, mock_keyup):
        result = self.keyboard.key_up("shift")
        self.assertEqual(result, "Released key: 'shift'.")
        mock_keyup.assert_called_once_with("shift")


class TestClipboardController(unittest.TestCase):

    def setUp(self):
        self.clipboard = ClipboardController()

    @patch("win32clipboard.OpenClipboard")
    @patch("win32clipboard.EmptyClipboard")
    @patch("win32clipboard.SetClipboardText")
    @patch("win32clipboard.CloseClipboard")
    def test_set_and_get_text(self, mock_close, mock_set, mock_empty, mock_open):
        result = self.clipboard.set_text("Test Clipboard")
        self.assertTrue(result)
        mock_open.assert_called_once()
        mock_empty.assert_called_once()
        mock_set.assert_called_once_with("Test Clipboard", 13) # CF_UNICODETEXT is 13
        mock_close.assert_called_once()

    @patch("win32clipboard.OpenClipboard")
    @patch("win32clipboard.GetClipboardData")
    @patch("win32clipboard.CloseClipboard")
    def test_get_text_success(self, mock_close, mock_get, mock_open):
        mock_get.return_value = "Retrieved Text"
        text = self.clipboard.get_text()
        self.assertEqual(text, "Retrieved Text")
        mock_open.assert_called_once()
        mock_get.assert_called_once_with(13)
        mock_close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
