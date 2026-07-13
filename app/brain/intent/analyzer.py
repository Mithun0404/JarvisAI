"""
Intent analyzer.
"""

from app.brain.intent.intents import Intent


class IntentAnalyzer:

    def analyze(self, text: str):

        text = text.lower()

        open_keywords = (

            "open",

            "launch",

            "start",

            "run",

        )

        if any(keyword in text for keyword in open_keywords):

            return Intent.OPEN_APPLICATION

        return Intent.GENERAL_CHAT