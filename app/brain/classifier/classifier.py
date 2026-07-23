"""
AI Intent Classifier.
"""

import json

from app.brain.providers.ollama_provider import OllamaProvider

from app.brain.classifier.prompts import (
    INTENT_CLASSIFIER_PROMPT,
)

from app.brain.classifier.schemas import (
    IntentClassification,
)

class IntentClassifier:

    def __init__(self, provider):

        self.provider = provider

    def classify(
        self,
        text: str,
    ) -> IntentClassification:

        response = self.provider.generate(

            INTENT_CLASSIFIER_PROMPT,

            text,

        )
       
        try:

            data = json.loads(response)

        except Exception:

            return IntentClassification()

        return IntentClassification(

            intent=data.get(
                "intent",
                "CHAT",
            ),

            parameters=data.get(
                "parameters",
                {},
            ),

            confidence=float(
                data.get(
                    "confidence",
                    0.0,
                )
            ),
        )