"""
Ollama AI provider for JARVIS.
"""

from ollama import chat

from app.brain.providers.base import AIProvider


class OllamaProvider(AIProvider):
    """
    AI provider that communicates with a local Ollama server.
    """

    def __init__(self, model: str = "llama3.2:1b"):

        self.model = model

    def chat(self, messages: list[dict]) -> str:
        """
        Send conversation history to Ollama and return
        the assistant response.
        """

        response = chat(
            model=self.model,
            messages=messages,
        )

        return response.message.content