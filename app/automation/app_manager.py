"""
Application Manager.

Provides capability to launch, scale, and close applications using the ApplicationRegistry.
"""

import os
import shutil
import subprocess
from typing import List, Optional
import win32gui
import win32process

from app.core.applications import registry, ApplicationDefinition


class ApplicationManager:
    """
    Manages process lifecycles and window associations for registered applications.
    """

    def __init__(self) -> None:
        pass

    def start_application(self, key: str) -> str:
        """
        Launches the application matching the given key.
        """
        app = registry.get(key)
        if not app:
            return f"Application '{key}' is not registered in the system registry."

        for path in app.executable_paths:
            # Check system PATH environment variable
            resolved_path = shutil.which(path)
            if resolved_path:
                try:
                    subprocess.Popen([resolved_path])
                    return f"Opening {app.display_name}..."
                except Exception as e:
                    return f"Failed to open {app.display_name} via {resolved_path}: {e}"

            # Check absolute path
            if os.path.exists(path):
                try:
                    subprocess.Popen([path])
                    return f"Opening {app.display_name}..."
                except Exception as e:
                    return f"Failed to open {app.display_name} via {path}: {e}"

        return f"Could not find {app.display_name} at any registered executable path."

    def close_application(self, key: str) -> str:
        """
        Terminates the application by its process name(s).
        """
        app = registry.get(key)
        if not app:
            return f"Application '{key}' is not registered in the system registry."

        errors = []
        success = False

        for proc_name in app.process_names:
            try:
                # Terminate processes using Windows taskkill command
                result = subprocess.run(
                    ["taskkill", "/F", "/IM", proc_name],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    success = True
                else:
                    errors.append(result.stderr.strip() or f"Process {proc_name} not found.")
            except Exception as e:
                errors.append(str(e))

        if success:
            return f"Closed {app.display_name}."
        
        return f"Failed to close {app.display_name}. Detail: " + "; ".join(errors)

    def get_application_windows(self, key: str) -> List[int]:
        """
        Finds all active window handles (hwnd) for the given application key.
        Matches window titles case-insensitively using the registered window names.
        """
        app = registry.get(key)
        if not app:
            return []

        matched_hwnds = []
        lower_patterns = [pat.lower() for pat in app.window_names]

        # Enumerate Windows to find matching title substrings or matching process IDs
        def enum_call(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).lower()
                for pat in lower_patterns:
                    if pat in title:
                        matched_hwnds.append(hwnd)
                        break
            return True

        win32gui.EnumWindows(enum_call, None)
        return matched_hwnds
