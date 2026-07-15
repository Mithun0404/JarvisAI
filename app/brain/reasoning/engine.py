"""
Reasoning Engine.
"""

from app.brain.reasoning.memory import MemoryReasoner
from app.brain.reasoning.tool import ToolReasoner
from app.brain.reasoning.chat import ChatReasoner


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

        # --------------------------------------------------
        # 1. Memory Questions
        # --------------------------------------------------

        response = self.memory_reasoner.resolve(
            user_input,
            memory,
        )

        if response is not None:
            return response

        # --------------------------------------------------
        # 2. Tool Requests
        # --------------------------------------------------

        response = self.tool_reasoner.resolve(
            user_input,
            intent,
            tool_manager,
        )

        if response is not None:
            return response

        # --------------------------------------------------
        # 3. Learn New Information
        # --------------------------------------------------

        facts = memory.learn(user_input)

        if facts:

            learned = ", ".join(
                f"{k} = {v}"
                for k, v in facts.items()
            )

            return (
                f"I'll remember that ({learned})."
            )

        # --------------------------------------------------
        # 4. Normal AI Conversation
        # --------------------------------------------------

        return self.chat_reasoner.resolve(
            provider,
            memory,
        )