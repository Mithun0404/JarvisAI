"""
Speech-To-Text (STT) Module for JARVIS.

Captures microphone audio input and transcribes spoken audio into text.
"""

from typing import Optional
from loguru import logger

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

    def __init__(self, energy_threshold: int = 300, pause_threshold: float = 0.8) -> None:
        """
        Initialize Speech Recognition engine.
        """
        if not STT_AVAILABLE:
            logger.warning("SpeechRecognition library is not installed.")
            self.recognizer = None
            return

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = energy_threshold
        self.recognizer.pause_threshold = pause_threshold

    def listen(self, timeout: Optional[float] = 5.0, phrase_time_limit: Optional[float] = 10.0) -> Optional[str]:
        """
        Listens to microphone input and converts speech to text.
        
        :param timeout: Maximum seconds to wait for speech to start.
        :param phrase_time_limit: Maximum seconds allowed for spoken phrase.
        :return: Transcribed text string if successful, None otherwise.
        """
        if not self.recognizer:
            logger.error("SpeechToText recognizer is not available.")
            return None

        try:
            with sr.Microphone() as source:
                logger.info("Listening for voice input...")
                # Calibrate for ambient noise quickly
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

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
