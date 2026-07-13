"""
Memory reasoning.
"""


class MemoryReasoner:

    MEMORY_QUESTIONS = {

        "what is my name": "name",

        "who am i": "name",

        "what's my name": "name",

    }

    def resolve(self, text, memory):

        key = self.MEMORY_QUESTIONS.get(
            text.lower()
        )

        if key is None:

            return None

        value = memory.recall(key)

        if value is None:

            return "I don't know yet."

        return f"Your {key} is {value}."