"""
Task Executor.
"""

import time

from app.tools.manager import ToolManager


class TaskExecutor:

    def __init__(self):

        self.tool_manager = ToolManager()

    def execute(self, plan):

        results = []

        for action in plan.actions:

            print("\n========== EXECUTOR ==========")
            print("Intent     :", action.intent)
            print("Parameters :", action.parameters)
            print("==============================")

            result = self.tool_manager.execute(
                action.intent,
                action.parameters,
            )

            print("Result:", result)

            results.append(result)

            if action.intent == "OPEN_APPLICATION":
                time.sleep(2)

        return results