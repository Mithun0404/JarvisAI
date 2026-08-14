"""
Speech-To-Text (STT) Module for JARVIS.

Captures microphone audio input and transcribes spoken audio into text.
"""

from typing import Optional
from loguru import logger

from app.core.config import settings

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    sr = None
    STT_AVAILABLE = False


class SpeechToText:
    """
    Handles audio recording and transcription from microphone input.
    """

    def __init__(self, energy_threshold: int = 300, pause_threshold: Optional[float] = None) -> None:
        """
        Initialize Speech Recognition engine.
        
        :param pause_threshold: Seconds of silence after speech stops before finalizing (default from settings: 3.0s - 5.0s).
        """
        if not STT_AVAILABLE:
            logger.warning("SpeechRecognition library is not installed.")
            self.recognizer = None
            return

        p_thresh = pause_threshold if pause_threshold is not None else getattr(settings, "stt_pause_threshold", 3.0)

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = p_thresh
        logger.info(f"SpeechToText initialized with pause threshold: {self.recognizer.pause_threshold}s")

    def set_pause_threshold(self, seconds: float = 3.0) -> None:
        """Set silence pause duration in seconds after user stops speaking."""
        if self.recognizer:
            self.recognizer.pause_threshold = max(0.5, float(seconds))
            logger.info(f"STT pause threshold updated to: {self.recognizer.pause_threshold}s")

    def listen(self, timeout: Optional[float] = None, phrase_time_limit: Optional[float] = None) -> Optional[str]:
        """
        Listens to microphone input and converts speech to text.
        
        :param timeout: Maximum seconds to wait for speech to start.
        :param phrase_time_limit: Maximum seconds allowed for spoken phrase.
        :return: Transcribed text string if successful, None otherwise.
        """
        if not self.recognizer:
            logger.error("SpeechToText recognizer is not available.")
            return None

        listen_timeout = timeout if timeout is not None else getattr(settings, "stt_timeout", 8.0)
        time_limit = phrase_time_limit if phrase_time_limit is not None else getattr(settings, "stt_phrase_time_limit", 15.0)

        try:
            with sr.Microphone() as source:
                logger.info("Listening for voice input...")
                # Calibrate for ambient noise quickly (0.2s for maximum speed)
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = self.recognizer.listen(source, timeout=listen_timeout, phrase_time_limit=time_limit)

            logger.info("Transcribing voice input...")
            # Use Google Speech Recognition API (free, built into speech_recognition)
            text = self.recognizer.recognize_google(audio)
            logger.success(f"Voice Transcribed: '{text}'")
            return text

        except sr.WaitTimeoutError:
            logger.warning("Listening timed out. No speech detected.")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio input.")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Microphone or STT error: {e}")
            return None
