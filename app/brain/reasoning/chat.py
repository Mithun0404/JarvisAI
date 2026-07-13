"""
General AI reasoning.
"""

from app.brain.prompt.builder import PromptBuilder


class ChatReasoner:

    def __init__(self):

        self.builder = PromptBuilder()

    def resolve(
        self,
        provider,
        memory,
    ):

        messages = self.builder.build(

            memory.facts(),

            memory.conversation(),

        )

        return provider.chat(messages)