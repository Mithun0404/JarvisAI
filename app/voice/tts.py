"""
Text-To-Speech (TTS) Module for JARVIS.

Uses Windows native SAPI5 via pywin32 for zero-latency, offline voice synthesis.
"""

from typing import Optional
import win32com.client
from loguru import logger


class TextToSpeech:
    """
    Handles speech synthesis for voice feedback.
    """

    def __init__(self, rate: int = 0, volume: int = 100) -> None:
        """
        Initialize SAPI5 voice speaker.
        
        :param rate: Speech rate modifier (-10 to 10). Default 0.
        :param volume: Speech volume (0 to 100). Default 100.
        """
        self.muted = False
        try:
            self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
            self.speaker.Rate = rate
            self.speaker.Volume = volume
            logger.info("TextToSpeech (SAPI5) initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize SAPI5 TTS engine: {e}")
            self.speaker = None

    def speak(self, text: str, async_speech: bool = False) -> bool:
        """
        Speaks the given text out loud.
        
        :param text: Text string to speak.
        :param async_speech: If True, speech runs asynchronously without blocking execution.
        :return: True if spoken successfully, False otherwise.
        """
        if self.muted:
            logger.debug("TTS is muted. Skipping speech output.")
            return False

        if not text or not text.strip():
            return False

        if not self.speaker:
            logger.warning("TTS speaker is not available.")
            return False

        try:
            # SAPI flags: 0 = Sync, 1 = Async
            flags = 1 if async_speech else 0
            self.speaker.Speak(text, flags)
            return True
        except Exception as err:
            logger.error(f"TTS Speech error: {err}")
            return False

    def set_rate(self, rate: int) -> None:
        """Set speech rate (-10 to 10)."""
        if self.speaker:
            self.speaker.Rate = max(-10, min(10, rate))

    def set_volume(self, volume: int) -> None:
        """Set speech volume (0 to 100)."""
        if self.speaker:
            self.speaker.Volume = max(0, min(100, volume))

    def set_muted(self, muted: bool) -> None:
        """Mute or unmute speech output."""
        self.muted = muted
        logger.info(f"TTS muted state set to: {self.muted}")
