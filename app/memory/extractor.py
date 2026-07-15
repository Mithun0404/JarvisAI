"""
AI memory extractor.
"""

import json

from app.brain.providers.ollama_provider import OllamaProvider

from app.memory.prompts import MEMORY_EXTRACTION_PROMPT

from app.memory.schemas import MemoryExtraction


class MemoryExtractor:

    def __init__(self, provider):

        self.provider = provider
        
    def extract(
        self,
        text: str,
    ) -> MemoryExtraction:

        response = self.provider.generate(

            MEMORY_EXTRACTION_PROMPT,

            text,

        )

        try:

            data = json.loads(response)

        except Exception:

            return MemoryExtraction()

        return MemoryExtraction(

            store=data.get("store", False),

            facts=data.get("facts", {}),

        )