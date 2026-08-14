"""
Text-To-Speech (TTS) Module for JARVIS.

Supports Microsoft Azure Neural Voices via edge-tts for realistic, sweet, and elegant speech,
with Windows SAPI5 as an offline fallback.
"""

import os
import io
import asyncio
import tempfile
import threading
from typing import Optional, Dict
import win32com.client
from loguru import logger

from app.core.config import settings
from app.voice.emotion import get_emotion_prosody, detect_emotion

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

# Global in-memory cache for synthesized audio bytes (0ms replay latency)
AUDIO_CACHE: Dict[str, bytes] = {}

try:
    import edge_tts
    import pygame
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False


NEURAL_VOICES = {
    # High Energy, Passionate & Expressive ("Josh") Voices
    "josh": "en-US-AndrewNeural",        # Energetic, passionate & confident speaker (Default Josh Voice)
    "andrew": "en-US-AndrewNeural",      # High-energy, confident male voice
    "brian": "en-US-BrianNeural",        # Lively, enthusiastic & dynamic male speaker
    "ava": "en-US-AvaNeural",            # Dynamic, upbeat & expressive female voice
    "emma": "en-US-EmmaNeural",          # Lively & enthusiastic female voice
    "neerja-expressive": "en-IN-NeerjaExpressiveNeural", # High-energy Indian English female voice

    # Clear & Natural Female Voices
    "aria": "en-US-AriaNeural",          # Sweet, warm & natural (US Female)
    "jenny": "en-US-JennyNeural",        # Friendly, clear, conversational (US Female)
    "sonia": "en-GB-SoniaNeural",        # Smooth, warm & elegant (British Female)
    "sallie": "en-GB-SallieNeural",      # Sophisticated (British Female)
    "emily": "en-IE-EmilyNeural",        # F.R.I.D.A.Y. accent (Irish Female)
    "friday": "en-IE-EmilyNeural",       # F.R.I.D.A.Y. from Iron Man
    "neerja": "en-IN-NeerjaNeural",      # Clear Indian English Female

    # Clear & Professional Male Voices (JARVIS style)
    "jarvis": "en-US-GuyNeural",         # Classic AI male voice (US Male)
    "guy": "en-US-GuyNeural",            # Crisp & natural (US Male)
    "christopher": "en-US-ChristopherNeural", # Deep, warm & professional (US Male)
    "ryan": "en-GB-RyanNeural",          # Elegant British male accent (GB Male)
    "steffan": "en-US-SteffanNeural",    # Calm & clear (US Male)
}

# Backward compatibility alias
NEURAL_FEMALE_VOICES = NEURAL_VOICES


class TextToSpeech:
    """
    Handles speech synthesis with high-clarity neural voices (Edge-TTS)
    and offline SAPI5 fallback.
    """

    def __init__(self, rate: int = 0, volume: int = 100, voice: Optional[str] = None) -> None:
        """
        Initialize TTS engine.
        
        :param rate: SAPI5 rate modifier (-10 to 10). Default 0.
        :param volume: Speech volume (0 to 100). Default 100.
        :param voice: Preferred neural voice or voice key (e.g. 'aria', 'jarvis', 'jenny', 'sonia').
        """
        self.muted = False
        default_voice = getattr(settings, "tts_voice", "en-US-AriaNeural")
        default_rate = getattr(settings, "tts_rate", "+0%")
        default_pitch = getattr(settings, "tts_pitch", "+0Hz")

        v_choice = voice or default_voice
        key = v_choice.lower()
        if key in NEURAL_VOICES:
            self.voice = NEURAL_VOICES[key]
        elif v_choice in NEURAL_VOICES.values():
            self.voice = v_choice
        else:
            self.voice = NEURAL_VOICES.get(key, default_voice)

        self.speech_rate = default_rate   # +0% natural speaking rate for maximum clarity
        self.speech_pitch = default_pitch # +0Hz standard natural pitch
        
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
            self._set_sapi5_voice()
        except Exception as e:
            logger.warning(f"Failed to initialize SAPI5 fallback: {e}")
            self.speaker = None

        logger.info(f"TextToSpeech initialized with neural voice: {self.voice} (speed: {self.speech_rate}, pitch: {self.speech_pitch})")

    def set_speech_rate(self, rate_percentage: int = 0) -> None:
        """Set speech speed percentage (e.g. 0 for normal, +10 for faster, -10 for slower)."""
        sign = "+" if rate_percentage >= 0 else ""
        self.speech_rate = f"{sign}{rate_percentage}%"
        logger.info(f"TTS speech speed rate set to: {self.speech_rate}")

    def set_pitch(self, pitch_hz: int = 0) -> None:
        """Set speech pitch modifier in Hz (e.g. +2Hz, -2Hz, 0Hz)."""
        sign = "+" if pitch_hz >= 0 else ""
        self.speech_pitch = f"{sign}{pitch_hz}Hz"
        logger.info(f"TTS pitch set to: {self.speech_pitch}")

    def enable_josh_mode(self, voice_key: str = "ava") -> None:
        """
        Activates high-energy, passionate speaker mode ("Josh").
        Increases pitch inflection (+3Hz) and rate (+8%) to eliminate flat lecture-style tone.
        Supports energetic female voices ('ava', 'emma', 'neerja-expressive') or male ('josh', 'andrew').
        """
        self.set_voice(voice_key)
        self.set_pitch(3)       # +3Hz pitch lift for energetic, passionate inflection
        self.set_speech_rate(8) # +8% confident, punchy cadence
        logger.info(f"High-Energy Passionate Mode activated with voice: {self.voice}")

    def _set_sapi5_voice(self) -> None:
        """Selects default voice in SAPI5 for offline fallback."""
        if not self.speaker:
            return
        try:
            voices = self.speaker.GetVoices()
            preferred_keywords = ["zira", "david", "female", "hazel", "eva", "catherine"]
            for i in range(voices.Count):
                v = voices.Item(i)
                desc = v.GetDescription().lower()
                if any(kw in desc for kw in preferred_keywords):
                    self.speaker.Voice = v
                    return
            if voices.Count > 0:
                self.speaker.Voice = voices.Item(0)
        except Exception as err:
            logger.debug(f"SAPI5 voice setting error: {err}")

    def set_voice(self, voice_name_or_key: str) -> bool:
        """
        Set the neural voice. You can pass keys like 'aria', 'jarvis', 'jenny', 'sonia', 'guy', 'ryan',
        or exact voice names like 'en-US-AriaNeural'.
        """
        key = voice_name_or_key.lower()
        if key in NEURAL_VOICES:
            self.voice = NEURAL_VOICES[key]
        else:
            self.voice = voice_name_or_key
        logger.info(f"TTS voice updated to: {self.voice}")
        return True

    def get_available_voices(self) -> dict:
        """Returns map of voice key presets to full neural voice names."""
        return NEURAL_VOICES

    def speak(self, text: str, async_speech: bool = False, emotion: Optional[str] = None) -> bool:
        """
        Speaks text using high-clarity neural voice (Edge-TTS) with automatic emotional prosody modulation.
        
        :param text: Text string to speak.
        :param async_speech: If True, speaks asynchronously without blocking execution.
        :param emotion: Optional explicit emotion override ('excited', 'happy', 'sad', 'apologetic', 'curious', 'serious', 'neutral').
        :return: True if spoken successfully, False otherwise.
        """
        if self.muted or not text or not text.strip():
            return False

        # Compute dynamic pitch, rate, and volume based on detected or specified emotion
        pitch, rate, volume, emotion_name = get_emotion_prosody(text, emotion)

        cache_key = f"{self.voice}:{pitch}:{rate}:{volume}:{text.strip()}"

        if self.use_edge_tts:
            try:
                def _generate_and_play():
                    async def _async_speak():
                        try:
                            if cache_key in AUDIO_CACHE:
                                audio_bytes = AUDIO_CACHE[cache_key]
                            else:
                                communicate = edge_tts.Communicate(
                                    text,
                                    self.voice,
                                    rate=rate,
                                    pitch=pitch,
                                    volume=volume,
                                )
                                audio_data = bytearray()
                                async for chunk in communicate.stream():
                                    if chunk["type"] == "audio":
                                        audio_data.extend(chunk["data"])
                                audio_bytes = bytes(audio_data)
                                if len(audio_bytes) > 0 and len(AUDIO_CACHE) < 300:
                                    AUDIO_CACHE[cache_key] = audio_bytes

                            if not audio_bytes:
                                return

                            if not pygame.mixer.get_init():
                                pygame.mixer.init()

                            audio_stream = io.BytesIO(audio_bytes)
                            pygame.mixer.music.load(audio_stream)
                            pygame.mixer.music.play()
                            while pygame.mixer.music.get_busy():
                                await asyncio.sleep(0.02)
                            pygame.mixer.music.unload()
                        except Exception as err:
                            logger.warning(f"Edge-TTS error: {err}. Falling back to SAPI5.")
                            self._speak_sapi5(text, async_speech=False)

                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_closed():
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                    loop.run_until_complete(_async_speak())

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
