"""
Ollama AI provider.
"""

from ollama import chat

from app.brain.providers.base import AIProvider


class OllamaProvider(AIProvider):
    """
    Local Ollama provider.
    """

    def __init__(self, model: str = "llama3.2:1b"):

        self.model = model

    def chat(
        self,
        messages: list[dict],
    ) -> str:

        response = chat(
            model=self.model,
            messages=messages,
        )

        return response.message.content

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        messages = [

            {
                "role": "system",
                "content": system_prompt,
            },

            {
                "role": "user",
                "content": user_prompt,
            },

        ]

        return self.chat(messages)