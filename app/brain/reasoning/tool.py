"""
Tool reasoning.
"""

from app.brain.intent.intents import Intent


class ToolReasoner:

    def resolve(
        self,
        user_input,
        intent,
        tool_manager,
    ):

        if intent != Intent.OPEN_APPLICATION:

            return None

        application = user_input.split()[-1]

        return tool_manager.execute(
            intent,
            application,
        )