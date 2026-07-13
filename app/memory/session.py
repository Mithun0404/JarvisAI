"""
Session memory for JARVIS.
"""


class SessionMemory:
    """
    Stores conversation messages for the current session.
    """

    def __init__(self):

        self._messages = []

    def add(self, role: str, content: str):

        self._messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    def messages(self):

        return self._messages

    def clear(self):

        self._messages.clear()