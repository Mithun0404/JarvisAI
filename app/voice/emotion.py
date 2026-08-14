"""
Emotion Detection & Vocal Modulation Module for JARVIS TTS.

Analyzes text sentiment and context to automatically modulate pitch, speed rate,
and volume for dynamic, expressive speech synthesis.
"""

from typing import Tuple, Dict

EMOTION_PROSODIES: Dict[str, Dict[str, str]] = {
    "excited": {
        "pitch": "+6Hz",
        "rate": "+12%",
        "volume": "+10%",
        "description": "High energy, enthusiastic, upbeat greeting & celebration",
    },
    "happy": {
        "pitch": "+4Hz",
        "rate": "+8%",
        "volume": "+5%",
        "description": "Warm, cheerful, positive success tone",
    },
    "sad": {
        "pitch": "-6Hz",
        "rate": "-12%",
        "volume": "-15%",
        "description": "Low pitch, slow pace, soft empathetic tone for sad occasions",
    },
    "apologetic": {
        "pitch": "-4Hz",
        "rate": "-8%",
        "volume": "-10%",
        "description": "Subdued, soft, sympathetic tone for errors or regrets",
    },
    "curious": {
        "pitch": "+5Hz",
        "rate": "+4%",
        "volume": "+0%",
        "description": "Inquisitive, rising pitch inflection for questions",
    },
    "serious": {
        "pitch": "-3Hz",
        "rate": "-4%",
        "volume": "+10%",
        "description": "Deep, authoritative, firm warning tone",
    },
    "neutral": {
        "pitch": "+3Hz",
        "rate": "+8%",
        "volume": "+0%",
        "description": "Standard energetic Josh tone",
    },
}


def detect_emotion(text: str) -> str:
    """
    Analyzes input text to determine emotional tone.
    
    :param text: Input string to analyze.
    :return: Emotion key ('excited', 'happy', 'sad', 'apologetic', 'curious', 'serious', 'neutral')
    """
    if not text:
        return "neutral"

    lower_text = text.lower().strip()

    # 1. Sad / Sorrow / Sympathy / Condolences
    sad_keywords = {
        "sorry to hear", "sad", "unfortunate", "unfortunately", "condolences", "grief",
        "tragic", "tragedy", "loss", "mourn", "heartbroken", "disappointed",
        "disappointment", "terrible news", "bad news", "depressed", "crying", "rip",
        "sadness", "sorrow", "regret to inform"
    }
    if any(kw in lower_text for kw in sad_keywords):
        return "sad"

    # 2. Apologetic / System Error / Failure
    apology_keywords = {
        "apologize", "forgive me", "my bad", "failed", "error occurred", "unable to",
        "could not complete", "oops", "mistake", "cannot process"
    }
    if any(kw in lower_text for kw in apology_keywords):
        return "apologetic"

    # 3. Excited / Greetings / Celebrations
    excited_keywords = {
        "welcome", "hello", "good morning", "good evening", "good afternoon",
        "hurray", "awesome", "fantastic", "amazing", "let's go", "bingo",
        "congratulations", "hooray", "jarvis online", "systems active", "boss",
        "poindexter", "commander", "captain", "thrilled", "unbelievable", "wohoo",
        "yippee", "brilliant work", "spectacular"
    }
    if any(kw in lower_text for kw in excited_keywords) or (lower_text.endswith("!") and len(lower_text) < 90):
        return "excited"

    # 4. Happy / Success / Accomplishment
    happy_keywords = {
        "great", "done", "success", "successfully", "completed", "working",
        "glad", "wonderful", "pleasure", "enjoy", "nice work", "superb", "perfect"
    }
    if any(kw in lower_text for kw in happy_keywords):
        return "happy"

    # 5. Serious / Warning / Critical Alert
    serious_keywords = {
        "warning", "caution", "alert", "critical", "danger", "hazard", "forbidden",
        "fatal error", "shutdown initiated", "emergency", "system fault"
    }
    if any(kw in lower_text for kw in serious_keywords):
        return "serious"

    # 6. Curious / Questioning
    if lower_text.startswith(("what", "why", "how", "where", "who", "when", "can i", "shall we", "would you")) or lower_text.endswith("?"):
        return "curious"

    return "neutral"


def get_emotion_prosody(text: str, override_emotion: str = None) -> Tuple[str, str, str, str]:
    """
    Returns (pitch, rate, volume, emotion_name) for a given text.
    """
    emotion = override_emotion.lower() if override_emotion else detect_emotion(text)
    prosody = EMOTION_PROSODIES.get(emotion, EMOTION_PROSODIES["neutral"])
    return prosody["pitch"], prosody["rate"], prosody["volume"], emotion
