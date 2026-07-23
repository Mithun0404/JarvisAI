"""
Screenshot Capture Module.

Wraps PyAutoGUI screen capture capabilities to capture screen states
and return localized file information.
"""

from datetime import datetime
import os
from typing import Dict, Any, Optional
import pyautogui


class ScreenshotCapture:
    """
    Handles capturing the screen and metadata tagging.
    """

    def __init__(self, storage_dir: str = "logs/screenshots") -> None:
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def capture(self, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Captures the current primary screen, saves it as a PNG file, and returns metadata.
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"screenshot_{timestamp}.png"

        output_path = os.path.abspath(os.path.join(self.storage_dir, filename))
        
        try:
            # Capture the screenshot using PyAutoGUI (assisted by Pillow)
            screenshot = pyautogui.screenshot()
            screenshot.save(output_path)
            
            width, height = screenshot.size
            return {
                "success": True,
                "path": output_path,
                "width": width,
                "height": height,
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
