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

        # -----------------------------
        # Open Application
        # -----------------------------
        if intent == "OPEN_APPLICATION":

            application = classification.parameters.get("application")

            if not application:
                return "Application not specified."

            return tool_manager.execute(
                intent,
                application,
            )

        # -----------------------------
        # Close Application
        # -----------------------------
        elif intent == "CLOSE_WINDOW":

            application = classification.parameters.get("application")

            if not application:
                return "Application not specified."

            return tool_manager.execute(
                intent,
                application,
            )

        # -----------------------------
        # Web Automation
        # -----------------------------
        elif intent == "WEB_AUTOMATION":

            return tool_manager.execute(
                intent,
                classification.parameters,
            )

        # -----------------------------
        # Desktop Automation
        # -----------------------------
        elif intent == "DESKTOP_AUTOMATION":

            return tool_manager.execute(
                intent,
                classification.parameters,
            )

        return None