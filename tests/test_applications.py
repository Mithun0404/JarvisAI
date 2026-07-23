"""
Unit tests for Application Registry and Management Module.
"""

import unittest
from unittest.mock import MagicMock, patch

from app.core.applications import registry, ApplicationDefinition, ApplicationRegistry
from app.automation.app_manager import ApplicationManager
from app.automation.window_manager import WindowManager


class TestApplicationRegistry(unittest.TestCase):

    def setUp(self):
        self.reg = ApplicationRegistry()

    def test_default_apps_registered(self):
        notepad = self.reg.get("notepad")
        self.assertIsNotNone(notepad)
        self.assertEqual(notepad.display_name, "Notepad")
        self.assertIn("notepad.exe", notepad.executable_paths)

        chrome = self.reg.get("chrome")
        self.assertIsNotNone(chrome)
        self.assertEqual(chrome.display_name, "Google Chrome")

    def test_custom_app_registration(self):
        custom_app = ApplicationDefinition(
            key="test_app",
            display_name="Test App",
            executable_paths=["testapp.exe"],
            process_names=["testapp.exe"],
            window_names=["Test App Window"]
        )
        self.reg.register(custom_app)
        retrieved = self.reg.get("test_app")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.display_name, "Test App")


class TestApplicationManager(unittest.TestCase):

    def setUp(self):
        self.manager = ApplicationManager()

    @patch("shutil.which")
    @patch("subprocess.Popen")
    def test_start_application_success_via_path(self, mock_popen, mock_which):
        mock_which.return_value = "C:\\Windows\\System32\\notepad.exe"
        
        # Test default notepad
        result = self.manager.start_application("notepad")
        self.assertIn("Opening Notepad", result)
        mock_popen.assert_called_once_with(["C:\\Windows\\System32\\notepad.exe"])

    @patch("shutil.which")
    def test_start_application_unregistered(self, mock_which):
        result = self.manager.start_application("non_existing_app")
        self.assertIn("not registered", result)

    @patch("subprocess.run")
    def test_close_application_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stderr="")
        
        result = self.manager.close_application("notepad")
        self.assertEqual(result, "Closed Notepad.")
        mock_run.assert_called_with(["taskkill", "/F", "/IM", "notepad.exe"], capture_output=True, text=True)

    @patch("subprocess.run")
    def test_close_application_failure(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stderr="Process not found.")
        
        result = self.manager.close_application("notepad")
        self.assertIn("Failed to close Notepad", result)


class TestWindowManager(unittest.TestCase):

    def setUp(self):
        self.wm = WindowManager()

    @patch("win32gui.IsWindow")
    @patch("win32gui.GetWindowRect")
    def test_get_window_rect(self, mock_rect, mock_is_window):
        mock_is_window.return_value = True
        mock_rect.return_value = (10, 20, 110, 120)  # left, top, right, bottom
        
        rect = self.wm.get_window_rect(12345)
        self.assertIsNotNone(rect)
        self.assertEqual(rect["x"], 10)
        self.assertEqual(rect["y"], 20)
        self.assertEqual(rect["width"], 100)
        self.assertEqual(rect["height"], 100)


if __name__ == "__main__":
    unittest.main()
