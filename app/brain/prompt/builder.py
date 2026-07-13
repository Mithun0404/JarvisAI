"""
Prompt builder.
"""

from app.brain.prompt.personality import SYSTEM_PROMPT
from app.brain.prompt.templates import memory_template


class PromptBuilder:

    def build(
        self,
        memory: dict,
        conversation: list[dict],
    ):

        messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }

        ]

        profile = memory_template(memory)

        if profile:

            messages.append(

                {
                    "role": "system",
                    "content": profile,
                }

            )

        messages.extend(conversation)

        return messages