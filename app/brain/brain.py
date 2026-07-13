"""
Brain module.
"""

from app.brain.intent.analyzer import IntentAnalyzer
from app.brain.intent.intents import Intent
from app.brain.providers.ollama_provider import OllamaProvider
from app.memory.manager import MemoryManager
from app.tools.manager import ToolManager
from app.brain.prompt.builder import PromptBuilder
from app.brain.reasoning import ReasoningEngine


class Brain:

    def __init__(self):

        self.provider = OllamaProvider()

        self.intent = IntentAnalyzer()

        self.tool_manager = ToolManager()

        self.memory = MemoryManager()

        self.reasoning = ReasoningEngine()

        self.prompt_builder = PromptBuilder()

    def think(self, user_input):

        self.memory.add_user(user_input)

        facts = self.memory.learn(user_input)

        if facts:

            learned = ", ".join(

                f"{k} = {v}"

                for k, v in facts.items()

            )

            response = (

                f"I'll remember that ({learned})."

            )

            self.memory.add_assistant(response)

            return response

        intent = self.intent.analyze(user_input)

        response = self.reasoning.resolve(

            user_input,

            intent,

            self.provider,

            self.memory,

            self.tool_manager,

        )

        self.memory.add_assistant(response)

        return response