"""
Unit tests for the Browser Control Module.
"""

import unittest
from unittest.mock import patch, MagicMock

from app.automation.browser_controller import BrowserController


class TestBrowserController(unittest.TestCase):

    def setUp(self):
        self.bc = BrowserController()

    @patch("webbrowser.open")
    def test_open_url(self, mock_web_open):
        result = self.bc.open_url("http://example.com")
        self.assertEqual(result, "Opened URL: 'http://example.com'")
        mock_web_open.assert_called_once_with("http://example.com")

    @patch("webbrowser.open")
    def test_search(self, mock_web_open):
        result = self.bc.search("Python units")
        self.assertEqual(result, "Opened URL: 'https://www.google.com/search?q=Python%20units'")
        mock_web_open.assert_called_once_with("https://www.google.com/search?q=Python%20units")

    def test_scroll_down(self):
        # Mock keyboard press
        self.bc.keyboard = MagicMock()
        result = self.bc.scroll(direction="down", amount=2)
        self.assertEqual(result, "Scrolled browser down by 2 keyboard pages.")
        self.assertEqual(self.bc.keyboard.press.call_count, 2)
        self.bc.keyboard.press.assert_has_calls([unittest.mock.call("pagedown"), unittest.mock.call("pagedown")])

    def test_scroll_up(self):
        # Mock keyboard press
        self.bc.keyboard = MagicMock()
        result = self.bc.scroll(direction="up", amount=1)
        self.assertEqual(result, "Scrolled browser up by 1 keyboard pages.")
        self.bc.keyboard.press.assert_called_once_with("pageup")

    def test_unsupported_scroll(self):
        result = self.bc.scroll(direction="sideways")
        self.assertIn("Unsupported scroll direction", result)

    def test_tab_actions(self):
        self.bc.keyboard = MagicMock()
        self.bc.new_tab()
        self.bc.keyboard.hotkey.assert_called_once_with("ctrl", "t")

        self.bc.keyboard.reset_mock()
        self.bc.close_tab()
        self.bc.keyboard.hotkey.assert_called_once_with("ctrl", "w")

    def test_navigation_actions(self):
        self.bc.keyboard = MagicMock()
        self.bc.go_back()
        self.bc.keyboard.hotkey.assert_called_once_with("alt", "left")

        self.bc.keyboard.reset_mock()
        self.bc.go_forward()
        self.bc.keyboard.hotkey.assert_called_once_with("alt", "right")


if __name__ == "__main__":
    unittest.main()
