"""
Wake Word Detector Module for JARVIS.

Continuously monitors microphone audio in short windows to detect trigger keywords
such as "Jarvis", "Hey Jarvis", or "Ok Jarvis".
"""

from typing import Tuple, Optional, Set
from loguru import logger

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    sr = None
    STT_AVAILABLE = False


class WakeWordDetector:
    """
    Detects wake words from live microphone audio.
    """

    DEFAULT_WAKE_WORDS: Set[str] = {
        "jarvis",
        "hey jarvis",
        "ok jarvis",
        "okay jarvis",
        "hi jarvis",
        "hello jarvis"
    }

    def __init__(self, wake_words: Optional[Set[str]] = None) -> None:
        """
        Initialize wake word detector.
        """
        self.wake_words = wake_words or self.DEFAULT_WAKE_WORDS
        if not STT_AVAILABLE:
            logger.warning("SpeechRecognition library not available for WakeWordDetector.")
            self.recognizer = None
            return

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 280
        self.recognizer.pause_threshold = 0.5

    def listen_for_wake_word(self, timeout: float = 3.0) -> Tuple[bool, Optional[str]]:
        """
        Listens for a short audio phrase to detect the wake word.
        
        :param timeout: Max seconds to wait for speech start.
        :return: (is_detected: bool, extracted_inline_command: Optional[str])
        """
        if not self.recognizer:
            return False, None

        try:
            with sr.Microphone() as source:
                # Fast ambient adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=5.0)

            # Recognize audio using fast Google STT engine
            text = self.recognizer.recognize_google(audio).strip()
            clean_text = text.lower()

            logger.debug(f"Wake listener heard: '{text}'")

            # Check if any wake word is in clean_text
            for ww in self.wake_words:
                if ww in clean_text:
                    logger.success(f"WAKE WORD DETECTED: '{ww}' in '{text}'")

                    # Extract inline command if spoken together (e.g. "hey jarvis open chrome")
                    idx = clean_text.find(ww)
                    inline_cmd = text[idx + len(ww):].strip(" ,.!?")
                    
                    return True, (inline_cmd if inline_cmd else None)

            return False, None

        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return False, None
        except Exception as e:
            logger.debug(f"Wake word listening error: {e}")
            return False, None
