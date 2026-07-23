"""
Window Manager.

Provides reusable window control capabilities on Windows using win32gui/win32con.
"""

from typing import Dict, List, Optional
import win32con
import win32gui
import win32process


class WindowManager:
    """
    Handles window discovery, focusing, resizing, and state changes.
    """

    def find_windows(self, title_pattern: str) -> List[int]:
        """
        Finds all top-level window handles (hwnds) containing the title pattern (case-insensitive).
        """
        matched_hwnds = []
        pattern = title_pattern.lower()

        def enum_windows_callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if pattern in title.lower():
                    matched_hwnds.append(hwnd)
            return True

        win32gui.EnumWindows(enum_windows_callback, None)
        return matched_hwnds

    def focus_window(self, hwnd: int) -> bool:
        """
        Brings the specified window handle to the foreground.
        """
        if not win32gui.IsWindow(hwnd):
            return False

        try:
            # If minimized, restore it
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            
            win32gui.SetForegroundWindow(hwnd)
            return True
        except Exception:
            # Fallback for complex foreground lock scenarios in Windows
            try:
                # Simulate Alt keypress to bypass Win32 focus lock restrictions
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                shell.SendKeys('%')
                win32gui.SetForegroundWindow(hwnd)
                return True
            except Exception:
                # Last resort: show window forcefully
                try:
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                    return True
                except Exception:
                    return False

    def resize_window(self, hwnd: int, width: int, height: int) -> bool:
        """
        Resizes the window to the specified width and height while keeping its top-left coordinates.
        """
        rect = self.get_window_rect(hwnd)
        if not rect:
            return False
        try:
            win32gui.MoveWindow(hwnd, rect["x"], rect["y"], width, height, True)
            return True
        except Exception:
            return False

    def move_window(self, hwnd: int, x: int, y: int) -> bool:
        """
        Moves the window to the specified top-left coordinates (x, y) preserving its width and height.
        """
        rect = self.get_window_rect(hwnd)
        if not rect:
            return False
        try:
            win32gui.MoveWindow(hwnd, x, y, rect["width"], rect["height"], True)
            return True
        except Exception:
            return False

    def maximize_window(self, hwnd: int) -> bool:
        """
        Maximizes the window.
        """
        if not win32gui.IsWindow(hwnd):
            return False
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return True
        except Exception:
            return False

    def minimize_window(self, hwnd: int) -> bool:
        """
        Minimizes the window.
        """
        if not win32gui.IsWindow(hwnd):
            return False
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return True
        except Exception:
            return False

    def close_window(self, hwnd: int) -> bool:
        """
        Attempts to close the window gracefully by sending a WM_CLOSE message.
        """
        if not win32gui.IsWindow(hwnd):
            return False
        try:
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            return True
        except Exception:
            return False

    def get_window_rect(self, hwnd: int) -> Optional[Dict[str, int]]:
        """
        Gets the coordinates and dimensions of the window.
        Returns:
            dict containing x, y, width, height or None if lookup fails.
        """
        if not win32gui.IsWindow(hwnd):
            return None
        try:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            return {
                "x": left,
                "y": top,
                "width": right - left,
                "height": bottom - top
            }
        except Exception:
            return None

    def get_window_info(self, hwnd: int) -> Optional[Dict]:
        """
        Gathers raw metadata details for a given window handle.
        """
        if not win32gui.IsWindow(hwnd):
            return None
        try:
            title = win32gui.GetWindowText(hwnd)
            rect = self.get_window_rect(hwnd)
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            return {
                "hwnd": hwnd,
                "title": title,
                "rect": rect,
                "pid": pid,
                "visible": win32gui.IsWindowVisible(hwnd)
            }
        except Exception:
            return None
