"""
Mock AI provider.
"""

from app.brain.providers.base import AIProvider


class MockProvider(AIProvider):
    """
    Temporary AI provider.
    """

    def chat(self, messages: list[dict]) -> str:

        last_message = messages[-1]["content"]

        return (
            f"I received your message:\n\n"
            f"'{last_message}'\n\n"
            "A real AI provider has not been connected yet."
        )