"""
Long-term memory.
"""

from app.memory.storage import JsonStorage


class LongTermMemory:

    def __init__(self):

        self.storage = JsonStorage()

        self.data = self.storage.load()

    def remember(self, key, value):

        self.data[key] = value

        self.storage.save(self.data)

    def recall(self, key):

        return self.data.get(key)

    def all(self):

        return self.data