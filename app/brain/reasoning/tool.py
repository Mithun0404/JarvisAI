"""
Tool reasoning.
"""


class ToolReasoner:

    def resolve(
        self,
        classification,
        tool_manager,
    ):

        intent = classification.intent

        if intent == "OPEN_APPLICATION":

            application = classification.parameters.get(
                "application"
            )

            if not application:
                return "Application not specified."

            return tool_manager.execute(
                intent,
                application,
            )

        elif intent == "SEARCH_WEB":

            query = classification.parameters.get(
                "query"
            )

            if not query:
                return "Search query missing."

            return tool_manager.execute(
                intent,
                query,
            )

        return None