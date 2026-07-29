"""
Text-To-Speech (TTS) Module for JARVIS.

Supports Microsoft Azure Neural Voices via edge-tts for realistic, sweet, and elegant speech,
with Windows SAPI5 as an offline fallback.
"""

import os
import asyncio
import tempfile
import threading
from typing import Optional
import win32com.client
from loguru import logger

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

try:
    import edge_tts
    import pygame
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False


NEURAL_FEMALE_VOICES = {
    "friday": "en-IE-EmilyNeural",    # F.R.I.D.A.Y. from Iron Man (Irish female accent - Default)
    "emily": "en-IE-EmilyNeural",     # F.R.I.D.A.Y. from Iron Man
    "aria": "en-US-AriaNeural",       # Sweet, warm, elegant & natural
    "jenny": "en-US-JennyNeural",     # Friendly, clear, conversational
    "sallie": "en-GB-SallieNeural",   # Elegant & sophisticated British accent
    "sonia": "en-GB-SoniaNeural",     # Smooth & warm British accent
    "natasha": "en-AU-NatashaNeural", # Smooth Australian accent
    "neerja": "en-IN-NeerjaNeural",   # Clear Indian English accent
}


class TextToSpeech:
    """
    Handles speech synthesis with sweet, elegant neural voices (Edge-TTS)
    and offline SAPI5 fallback. Default: F.R.I.D.A.Y. (en-IE-EmilyNeural).
    """

    def __init__(self, rate: int = 0, volume: int = 100, voice: str = "en-IE-EmilyNeural") -> None:
        """
        Initialize TTS engine.
        
        :param rate: Speech rate modifier (-10 to 10). Default 0.
        :param volume: Speech volume (0 to 100). Default 100.
        :param voice: Preferred neural voice or voice key (default: en-IE-EmilyNeural / F.R.I.D.A.Y.).
        """
        self.muted = False
        self.voice = voice if voice in NEURAL_FEMALE_VOICES.values() else NEURAL_FEMALE_VOICES.get(voice.lower(), "en-IE-EmilyNeural")
        self.speech_rate = "+25%"  # Fast, crisp, responsive speaking speed
        
        # Initialize pygame mixer for audio playback
        self.use_edge_tts = HAS_EDGE_TTS
        if HAS_EDGE_TTS:
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
            except Exception as e:
                logger.warning(f"Failed to initialize pygame.mixer: {e}")
                self.use_edge_tts = False

        # Initialize SAPI5 fallback
        try:
            self.speaker = win32com.client.Dispatch("SAPI.SpVoice")
            self.speaker.Rate = max(-10, min(10, rate))
            self.speaker.Volume = volume
            self._set_sapi5_female_voice()
        except Exception as e:
            logger.warning(f"Failed to initialize SAPI5 fallback: {e}")
            self.speaker = None

        logger.info(f"TextToSpeech initialized with neural voice: {self.voice} (speed: {self.speech_rate})")

    def set_speech_rate(self, rate_percentage: int = 25) -> None:
        """Set speech speed percentage (e.g. 25 for +25% faster)."""
        sign = "+" if rate_percentage >= 0 else ""
        self.speech_rate = f"{sign}{rate_percentage}%"
        logger.info(f"TTS speech speed rate set to: {self.speech_rate}")

    def _set_sapi5_female_voice(self) -> None:
        """Selects female voice in SAPI5 for offline fallback."""
        if not self.speaker:
            return
        try:
            voices = self.speaker.GetVoices()
            female_keywords = ["zira", "female", "hazel", "eva", "heera", "catherine"]
            for i in range(voices.Count):
                voice = voices.Item(i)
                desc = voice.GetDescription().lower()
                if any(kw in desc for kw in female_keywords):
                    self.speaker.Voice = voice
                    return
            if voices.Count > 1:
                self.speaker.Voice = voices.Item(1)
        except Exception as err:
            logger.debug(f"SAPI5 female voice setting error: {err}")

    def set_voice(self, voice_name_or_key: str) -> bool:
        """
        Set the neural voice. You can pass 'aria', 'jenny', 'sallie', 'sonia',
        or exact voice names like 'en-US-AriaNeural'.
        """
        key = voice_name_or_key.lower()
        if key in NEURAL_FEMALE_VOICES:
            self.voice = NEURAL_FEMALE_VOICES[key]
        else:
            self.voice = voice_name_or_key
        logger.info(f"TTS voice updated to: {self.voice}")
        return True

    def speak(self, text: str, async_speech: bool = False) -> bool:
        """
        Speaks text using sweet, elegant neural voice (Edge-TTS) with SAPI5 fallback.
        
        :param text: Text string to speak.
        :param async_speech: If True, speaks asynchronously without blocking execution.
        :return: True if spoken successfully, False otherwise.
        """
        if self.muted or not text or not text.strip():
            return False

        if self.use_edge_tts:
            try:
                def _generate_and_play():
                    async def _async_speak():
                        temp_dir = tempfile.gettempdir()
                        temp_file = os.path.join(temp_dir, f"jarvis_tts_{os.getpid()}_{id(text)}.mp3")
                        try:
                            communicate = edge_tts.Communicate(text, self.voice, rate=self.speech_rate)
                            await communicate.save(temp_file)

                            if not pygame.mixer.get_init():
                                pygame.mixer.init()

                            pygame.mixer.music.load(temp_file)
                            pygame.mixer.music.play()
                            while pygame.mixer.music.get_busy():
                                await asyncio.sleep(0.05)
                            pygame.mixer.music.unload()
                        except Exception as err:
                            logger.warning(f"Edge-TTS error: {err}. Falling back to SAPI5.")
                            self._speak_sapi5(text, async_speech=False)
                        finally:
                            if os.path.exists(temp_file):
                                try:
                                    os.remove(temp_file)
                                except Exception:
                                    pass

                    asyncio.run(_async_speak())

                if async_speech:
                    threading.Thread(target=_generate_and_play, daemon=True).start()
                else:
                    _generate_and_play()
                return True
            except Exception as e:
                logger.error(f"Edge-TTS execution failed: {e}. Attempting SAPI5 fallback.")

        return self._speak_sapi5(text, async_speech)

    def _speak_sapi5(self, text: str, async_speech: bool = False) -> bool:
        """Fallback SAPI5 speech synthesis."""
        if not self.speaker:
            logger.warning("No TTS engine available.")
            return False
        try:
            flags = 1 if async_speech else 0
            self.speaker.Speak(text, flags)
            return True
        except Exception as err:
            logger.error(f"SAPI5 TTS error: {err}")
            return False

    def set_rate(self, rate: int) -> None:
        """Set speech rate modifier for SAPI5 fallback."""
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
