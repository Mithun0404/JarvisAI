"""
Automatic memory extraction.
"""

import re


class MemoryExtractor:
    """
    Extracts important user facts from natural language.
    """

    def extract(self, text: str) -> dict:

        memory = {}

        patterns = [

            (
                r"my name is (.+)",
                "name",
            ),

            (
                r"i am working on (.+)",
                "current_project",
            ),

            (
                r"i'm working on (.+)",
                "current_project",
            ),

            (
                r"my favorite language is (.+)",
                "favorite_language",
            ),

            (
                r"i like (.+)",
                "likes",
            ),

        ]

        text = text.strip().lower()

        for pattern, key in patterns:

            match = re.search(pattern, text)

            if match:

                value = match.group(1).strip()

                memory[key] = value.title()

        return memory