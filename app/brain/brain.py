"""
Brain module.
"""

from app.brain.history import ConversationHistory
from app.brain.providers.mock import MockProvider


class Brain:

    def __init__(self):

        self.history = ConversationHistory()

        self.provider = MockProvider()

    def think(self, user_input: str):

        self.history.add_user(user_input)

        response = self.provider.chat(
            self.history.get_messages()
        )

        self.history.add_assistant(response)

        return response