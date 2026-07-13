"""
Reasoning engine.
"""

from app.brain.reasoning.chat import ChatReasoner
from app.brain.reasoning.memory import MemoryReasoner
from app.brain.reasoning.tool import ToolReasoner


class ReasoningEngine:

    def __init__(self):

        self.memory_reasoner = MemoryReasoner()

        self.tool_reasoner = ToolReasoner()

        self.chat_reasoner = ChatReasoner()

    def resolve(

        self,

        user_input,

        intent,

        provider,

        memory,

        tool_manager,

    ):

        response = self.memory_reasoner.resolve(

            user_input,

            memory,

        )

        if response:

            return response

        response = self.tool_reasoner.resolve(

            user_input,

            intent,

            tool_manager,

        )

        if response:

            return response

        return self.chat_reasoner.resolve(

            provider,

            memory,

        )