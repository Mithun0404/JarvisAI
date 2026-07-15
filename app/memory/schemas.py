"""
Schemas used by the memory system.
"""

from dataclasses import dataclass, field


@dataclass
class MemoryExtraction:

    store: bool = False

    facts: dict = field(default_factory=dict)