"""
Screen Observer Module.

Combines window state discovery and screenshot metadata to present a
unified screen snapshot representation for reasoning.
"""

from typing import Dict, Any, List
import win32gui
import win32process

from app.automation.window_manager import WindowManager
from app.core.applications import registry
from app.vision.screenshot import ScreenshotCapture


class ScreenObserver:
    """
    Monitors, observes, and summarizes the system desktop state.
    """

    def __init__(self, screenshot_dir: str = "logs/screenshots") -> None:
        self.screenshot_capture = ScreenshotCapture(screenshot_dir)
        self.window_manager = WindowManager()

    def observe(self) -> Dict[str, Any]:
        """
        Takes a screenshot, fetches all visible window descriptions, detects registered tasks,
        and constructs a structured state representation.
        """
        # Capture screenshot
        screenshot_meta = self.screenshot_capture.capture()
        
        # Get active window handles
        visible_windows = []
        focused_hwnd = win32gui.GetForegroundWindow()
        
        def enum_call(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).strip()
                if title:
                    info = self.window_manager.get_window_info(hwnd)
                    if info:
                        # Add focused flag
                        info["is_focused"] = (hwnd == focused_hwnd)
                        visible_windows.append(info)
            return True

        win32gui.EnumWindows(enum_call, None)

        # Match visible windows against our application registry
        detected_apps = []
        for app_def in registry.list_apps():
            app_windows = []
            for win in visible_windows:
                # If window title contains app key or app window title signatures
                matched = False
                for p in app_def.window_names:
                    if p.lower() in win["title"].lower():
                        matched = True
                        break
                if matched:
                    app_windows.append(win)
            
            if app_windows:
                detected_apps.append({
                    "app_key": app_def.key,
                    "display_name": app_def.display_name,
                    "windows": app_windows
                })

        # Build analysis summary explanation text
        focused_app_desc = "None"
        for app in detected_apps:
            for w in app["windows"]:
                if w.get("is_focused"):
                    focused_app_desc = f"{app['display_name']} ('{w['title']}')"
                    break

        summary = f"Desktop State Observation:\n"
        summary += f"- Focused Window: {focused_app_desc}\n"
        summary += f"- Visible Windows:\n"
        for win in visible_windows[:7]:  # limit output length for LLM token economy
            focus_star = " [FOCUSED]" if win.get("is_focused") else ""
            summary += f"  * '{win['title']}' (PID: {win['pid']}){focus_star}\n"
        if len(visible_windows) > 7:
            summary += f"  * ... and {len(visible_windows) - 7} other windows.\n"

        return {
            "screenshot": screenshot_meta,
            "visible_windows": visible_windows,
            "detected_apps": detected_apps,
            "summary_text": summary
        }
