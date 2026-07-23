"""
Unit tests for the Vision & Desktop State Observation module.
"""

import os
import unittest
from unittest.mock import patch, MagicMock

from app.vision.screenshot import ScreenshotCapture
from app.vision.observer import ScreenObserver


class TestScreenshotCapture(unittest.TestCase):

    def setUp(self):
        self.capture_tool = ScreenshotCapture(storage_dir="logs/test_screenshots")

    def tearDown(self):
        # Clean up test directories if needed
        pass

    @patch("pyautogui.screenshot")
    def test_capture_success(self, mock_screenshot):
        mock_image = MagicMock()
        mock_image.size = (1920, 1080)
        mock_screenshot.return_value = mock_image

        result = self.capture_tool.capture(filename="test_img.png")
        self.assertTrue(result["success"])
        self.assertEqual(result["width"], 1920)
        self.assertEqual(result["height"], 1080)
        self.assertIn("test_img.png", result["path"])
        mock_image.save.assert_called_once()

    @patch("pyautogui.screenshot")
    def test_capture_failure(self, mock_screenshot):
        mock_screenshot.side_effect = Exception("Screenshot hardware error")

        result = self.capture_tool.capture(filename="test_fail.png")
        self.assertFalse(result["success"])
        self.assertIn("Screenshot hardware error", result["error"])


class TestScreenObserver(unittest.TestCase):

    def setUp(self):
        self.observer = ScreenObserver(screenshot_dir="logs/test_screenshots")

    @patch("app.vision.screenshot.ScreenshotCapture.capture")
    @patch("win32gui.GetForegroundWindow")
    @patch("win32gui.IsWindowVisible")
    @patch("win32gui.GetWindowText")
    @patch("win32gui.EnumWindows")
    @patch("app.automation.window_manager.WindowManager.get_window_info")
    def test_observe(self, mock_info, mock_enum, mock_text, mock_visible, mock_fg, mock_capture):
        # Setup mocks
        mock_capture.return_value = {
            "success": True,
            "path": "test_path.png",
            "width": 1920,
            "height": 1080
        }
        mock_fg.return_value = 1001
        
        # Simulate active windows call
        def fake_enum(callback, extra):
            callback(1001, None)  # notepad
            callback(1002, None)  # chrome
            return True
        mock_enum.side_effect = fake_enum
        
        mock_visible.return_value = True
        
        # Side effect for window text
        mock_text.side_effect = ["Untitled - Notepad", "New Tab - Google Chrome"]
        
        # Side effect for window info
        mock_info.side_effect = [
            {"hwnd": 1001, "title": "Untitled - Notepad", "rect": {"x": 0, "y": 0, "width": 800, "height": 600}, "pid": 456},
            {"hwnd": 1002, "title": "New Tab - Google Chrome", "rect": {"x": 100, "y": 100, "width": 1024, "height": 768}, "pid": 789}
        ]

        obs = self.observer.observe()
        
        self.assertIsNotNone(obs["screenshot"])
        self.assertEqual(len(obs["visible_windows"]), 2)
        self.assertTrue(obs["visible_windows"][0]["is_focused"])
        self.assertFalse(obs["visible_windows"][1]["is_focused"])
        
        # Verify application matching
        detected_keys = [app["app_key"] for app in obs["detected_apps"]]
        self.assertIn("notepad", detected_keys)
        self.assertIn("chrome", detected_keys)
        
        # Check summary formatting contains elements
        self.assertIn("Untitled - Notepad", obs["summary_text"])
        self.assertIn("Google Chrome", obs["summary_text"])


if __name__ == "__main__":
    unittest.main()
