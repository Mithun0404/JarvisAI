"""
News fetching and summarization service.

Fetches live headlines from Google News RSS (no API key required) and
asks the LLM to turn them into a short, spoken-style briefing.
"""

import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import Optional

from loguru import logger

GOOGLE_NEWS_RSS = "https://news.google.com/rss"


def _strip_html(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text or "").strip()


class NewsService:
    """
    Fetches current headlines and summarizes them into a spoken briefing.
    """

    def __init__(self, provider):
        self.provider = provider

    def fetch_headlines(self, topic: Optional[str] = None, limit: int = 8) -> list[dict]:
        if topic:
            url = f"{GOOGLE_NEWS_RSS}/search?q={urllib.parse.quote(topic)}&hl=en-IN&gl=IN&ceid=IN:en"
        else:
            url = f"{GOOGLE_NEWS_RSS}?hl=en-IN&gl=IN&ceid=IN:en"

        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

        try:
            with urllib.request.urlopen(request, timeout=8) as response:
                data = response.read()
        except Exception as err:
            logger.error(f"Failed to fetch news feed: {err}")
            return []

        try:
            root = ET.fromstring(data)
        except ET.ParseError as err:
            logger.error(f"Failed to parse news feed: {err}")
            return []

        headlines = []
        for item in root.findall(".//item")[:limit]:
            title = (item.findtext("title") or "").strip()
            description = _strip_html(item.findtext("description") or "")
            source = (item.findtext("source") or "").strip()

            if title:
                headlines.append({
                    "title": title,
                    "description": description,
                    "source": source,
                })

        return headlines

    def summarize(self, topic: Optional[str] = None) -> str:
        headlines = self.fetch_headlines(topic)

        if not headlines:
            subject = f" about {topic}" if topic else ""
            return f"I couldn't fetch any news{subject} right now. Please check your internet connection."

        listing = "\n".join(
            f"{i + 1}. {h['title']} ({h['source']})"
            for i, h in enumerate(headlines)
        )

        subject = f"about {topic}" if topic else "for today"

        prompt = (
            f"Here are the latest news headlines {subject}:\n\n{listing}\n\n"
            "Summarize these into a short, natural, spoken-style news briefing "
            "(4-6 sentences). Group related stories together where it makes sense. "
            "Do not just read the headlines verbatim, and do not use markdown, "
            "bullet points, or numbering -- write it exactly as it should be read aloud."
        )

        return self.provider.generate(
            system_prompt="You are JARVIS, briefing the user on the news concisely and naturally, like a news anchor.",
            user_prompt=prompt,
        )
