"""
Ollama AI provider.
"""

from ollama import chat

from app.brain.providers.base import AIProvider
from app.core.config import settings


class OllamaProvider(AIProvider):
    """
    Local Ollama provider.
    """

    def __init__(self, model: str | None = None):

        self.model = model or settings.brain_model

    def chat(
        self,
        messages: list[dict],
        json_mode: bool = False,
    ) -> str:

        response = chat(
            model=self.model,
            messages=messages,
            format="json" if json_mode else None,
            options={
                "temperature": settings.brain_temperature,
                "num_ctx": settings.brain_num_ctx,
            },
        )

        return response.message.content

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        json_mode: bool = False,
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

        return self.chat(messages, json_mode=json_mode)