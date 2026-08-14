"""
Browser Controller Module.

Provides reusable browser control primitives.
"""

import time
from urllib.parse import quote
import webbrowser

from app.automation.keyboard import KeyboardController
from app.automation.mouse import MouseController

# Minimum seconds between two play_youtube calls before a new tab is allowed.
# Guards against repeat triggers (e.g. the agent loop retrying, or a voice
# session picking up the playing video's own audio as a new command) opening
# a pile of tabs instead of reusing the one already playing.
PLAY_YOUTUBE_COOLDOWN_SECONDS = 20.0


class BrowserController:
    """
    Handles higher level web automation capabilities.
    """

    def __init__(self) -> None:
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self._last_play_time = 0.0

    def open_url(self, url: str) -> str:
        """
        Opens a specified URL in the default browser.
        """
        webbrowser.open(url)
        return f"Opened URL: '{url}'"

    def search(self, query: str) -> str:
        """
        Performs a Google Search in the default web browser.
        """
        encoded_query = quote(query)
        url = f"https://www.google.com/search?q={encoded_query}"
        return self.open_url(url)

    def play_youtube(self, query: str) -> str:
        """
        Searches and plays a song or video on YouTube directly in the default browser.
        """
        now = time.time()
        if now - self._last_play_time < PLAY_YOUTUBE_COOLDOWN_SECONDS:
            return "Already playing something on YouTube -- let me know if you want to switch tracks."
        self._last_play_time = now

        import re
        raw_text = query.lower().strip()
        prefixes = [
            "can you play", "could you play", "would you play", "please play",
            "play me", "play a song", "play song", "play music", "play a video", "play"
        ]
        for p in prefixes:
            if raw_text.startswith(p):
                raw_text = raw_text[len(p):].strip()

        suffixes = ["in youtube", "on youtube", "over youtube", "from youtube", "youtube", "song", "video", "track"]
        for s in suffixes:
            if raw_text.endswith(s):
                raw_text = raw_text[:-len(s)].strip()

        clean_query = raw_text.replace("in youtube", "").replace("on youtube", "").replace("over youtube", "").replace("youtube", "").replace(" song", "").strip()
        song_title = clean_query.title() if clean_query else "Popular Music"

        search_term = f"{clean_query} song" if clean_query else "popular music songs"
        video_url = f"https://www.youtube.com/results?search_query={quote(search_term)}"

        try:
            import urllib.request
            request = urllib.request.Request(
                f"https://www.youtube.com/results?search_query={quote(search_term)}",
                headers={
                    # A browser-like User-Agent + pre-accepted consent cookie avoids YouTube's
                    # bot-detection / cookie-consent redirect, which otherwise returns a page
                    # with no video results and silently breaks scraping.
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Cookie": "CONSENT=YES+1",
                },
            )
            html = urllib.request.urlopen(request, timeout=6.0).read().decode('utf-8', errors='ignore')
            video_ids = re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html)
            if video_ids:
                # Autoplay so the video starts immediately instead of landing on a paused page.
                video_url = f"https://www.youtube.com/watch?v={video_ids[0]}&autoplay=1"
        except Exception:
            pass

        webbrowser.open(video_url)
        return f"Gotcha! Playing {song_title} on YouTube now."

    def scroll(self, direction: str = "down", amount: int = 3) -> str:
        """
        Scrolls the screen using standard keyboard page events or mouse scrolls.
        """
        direction = direction.lower()
        if direction == "down":
            for _ in range(amount):
                self.keyboard.press("pagedown")
            return f"Scrolled browser down by {amount} keyboard pages."
        elif direction == "up":
            for _ in range(amount):
                self.keyboard.press("pageup")
            return f"Scrolled browser up by {amount} keyboard pages."
        else:
            return f"Unsupported scroll direction: '{direction}'."

    def new_tab(self) -> str:
        """
        Opens a new tab in the active browser using Ctrl+T.
        """
        self.keyboard.hotkey("ctrl", "t")
        return "Opened new browser tab."

    def close_tab(self) -> str:
        """
        Closes the active browser tab using Ctrl+W.
        """
        self.keyboard.hotkey("ctrl", "w")
        return "Closed active browser tab."

    def go_back(self) -> str:
        """
        Navigates back in history (Alt + Left).
        """
        self.keyboard.hotkey("alt", "left")
        return "Navigated back in browser history."

    def go_forward(self) -> str:
        """
        Navigates forward in history (Alt + Right).
        """
        self.keyboard.hotkey("alt", "right")
        return "Navigated forward in browser history."
