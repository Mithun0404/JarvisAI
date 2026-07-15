"""
Brain module.
"""

from app.brain.classifier import IntentClassifier
from app.brain.providers.ollama_provider import OllamaProvider
from app.brain.reasoning import ReasoningEngine
from app.memory.manager import MemoryManager
from app.tools.manager import ToolManager


class Brain:

    def __init__(self):

        self.provider = OllamaProvider()

        self.memory = MemoryManager(
            self.provider
        )

        self.tool_manager = ToolManager()

        self.reasoning = ReasoningEngine()

        self.classifier = IntentClassifier(
            self.provider
        )

    def think(self, user_input: str):

        self.memory.add_user(user_input)

        classification = self.classifier.classify(
            user_input
        )

        response = self.reasoning.resolve(
            user_input=user_input,
            classification=classification,
            provider=self.provider,
            memory=self.memory,
            tool_manager=self.tool_manager,
        )

        self.memory.add_assistant(response)

        return response