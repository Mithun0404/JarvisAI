"""
Intent classification schema.
"""

from dataclasses import dataclass, field


@dataclass
class IntentClassification:
    """
    Result returned by the AI intent classifier.
    """

    intent: str = "CHAT"

    parameters: dict = field(default_factory=dict)

    confidence: float = 0.0