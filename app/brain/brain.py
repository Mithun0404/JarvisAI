"""
Brain module.
"""

from app.brain.history import ConversationHistory
from app.brain.providers.ollama_provider import OllamaProvider
from app.tools.manager import ToolManager
from app.brain.intent.analyzer import IntentAnalyzer
from app.brain.intent.intents import Intent


class Brain:

    def __init__(self):

        self.history = ConversationHistory()

        self.provider = OllamaProvider()
        
        self.tool_manager = ToolManager()

        self.intent = IntentAnalyzer()

    def think(self, user_input: str):

        self.history.add_user(user_input)

        intent = self.intent.analyze(user_input)

        if intent.name.startswith("OPEN"):

            application = user_input.split()[-1]

            response = self.tool_manager.execute(
                intent,
                application,
            )

        else:

            response = self.provider.chat(
                self.history.get_messages()
            )

        self.history.add_assistant(response)

        return response