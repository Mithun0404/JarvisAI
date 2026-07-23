"""
AI Task Planner.
"""

import json

from app.brain.providers.ollama_provider import OllamaProvider
from app.planner.prompts import PLANNER_PROMPT
from app.planner.schemas import Action, Plan


class TaskPlanner:

    def __init__(self, provider=None):

        self.provider = provider or OllamaProvider()

    def create_plan(self, user_input: str) -> Plan:

        response = self.provider.generate(
            PLANNER_PROMPT,
            user_input,
        )

        try:

            data = json.loads(response)

        except Exception:

            return Plan()

        actions = []

        for item in data.get("actions", []):

            actions.append(
                Action(
                    intent=item.get("intent", ""),
                    parameters=item.get("parameters", {}),
                )
            )

        return Plan(actions)