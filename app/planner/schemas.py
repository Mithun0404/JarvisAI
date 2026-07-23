"""
Planner schemas.
"""

from dataclasses import dataclass, field


@dataclass
class Action:

    intent: str

    parameters: dict = field(default_factory=dict)


@dataclass
class Plan:

    actions: list[Action] = field(default_factory=list)