"""
Memory manager.
"""

from app.memory.long_term import LongTermMemory
from app.memory.session import SessionMemory
from app.memory.extractor import MemoryExtractor
from app.tools.application_tool import ApplicationTool
from app.tools.browser_tool import BrowserTool


class MemoryManager:

    def __init__(self,provider):

        self.session = SessionMemory()

        self.long_term = LongTermMemory()

    
        self.extractor = MemoryExtractor(provider)
        
    
    def learn(self,text: str,):

        extraction = self.extractor.extract(text)

        if not extraction.store:

            return {}

        for key, value in extraction.facts.items():

            self.long_term.remember(key,value,)

        return extraction.facts

    def add_user(self, message):

        self.session.add(
            "user",
            message,
        )

    def add_assistant(self, message):

        self.session.add(
            "assistant",
            message,
        )

    def conversation(self):

        return self.session.messages()

    def remember(self, key, value):

        self.long_term.remember(
            key,
            value,
        )

    def recall(self, key):

        return self.long_term.recall(
            key,
        )

    def clear(self):

        self.session.clear()
    
    def facts(self):

        return self.long_term.all()