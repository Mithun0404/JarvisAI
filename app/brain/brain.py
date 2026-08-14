"""
Brain module.
"""

import string

from app.brain.classifier import IntentClassifier
from app.brain.providers.ollama_provider import OllamaProvider
from app.brain.reasoning import ReasoningEngine
from app.brain.agent_loop import AgentLoop
from app.core.applications import registry
from app.memory.manager import MemoryManager
from app.tools.manager import ToolManager
from app.services.news_service import NewsService

# Phrases that signal the user is correcting the previous command, ordered
# longest-first so a specific marker is matched before a shorter generic one.
CORRECTION_MARKERS = [
    "no, i meant", "no i meant", "no, i said", "no i said",
    "that's not what i meant", "that's not what i said",
    "not what i meant", "not what i said",
    "actually i meant", "i meant", "i said",
    "that's wrong", "no,", "no ",
]


class Brain:

    def __init__(self):

        self.provider = OllamaProvider()

        self.memory = MemoryManager(
            self.provider
        )

        self.tool_manager = ToolManager()

        self.reasoning = ReasoningEngine()

        self.classifier = IntentClassifier(
            self.provider
        )

        self.agent_loop = AgentLoop(
            self.provider,
            self.memory
        )

        self.news_service = NewsService(
            self.provider
        )

    def think(self, user_input: str):

        self.memory.add_user(user_input)

        # --------------------------------------------------
        # If this exact command previously got corrected, use
        # the learned correction instead of re-guessing.
        # --------------------------------------------------
        learned_goal = self.memory.get_correction(user_input)
        if learned_goal:
            response = self._route(learned_goal)
            self.memory.add_assistant(response)
            return response

        # --------------------------------------------------
        # If the user is correcting the previous command, learn
        # the mapping and act on the corrected instruction.
        # --------------------------------------------------
        correction_target = self._extract_correction(user_input)
        if correction_target is not None:
            previous_input = self._last_user_message()

            if previous_input and correction_target:
                self.memory.save_correction(previous_input, correction_target)
                response = f"Got it, I'll remember that. {self._route(correction_target)}"
            else:
                response = "Got it -- what would you like me to do instead?"

            self.memory.add_assistant(response)
            return response

        response = self._route(user_input)
        self.memory.add_assistant(response)
        return response

    def _last_user_message(self):
        """Finds the user message immediately preceding the current one."""
        messages = self.memory.conversation()
        for entry in reversed(messages[:-1]):
            if entry.get("role") == "user":
                return entry.get("content")
        return None

    @staticmethod
    def _extract_correction(user_input: str):
        """
        Returns the corrected instruction text if `user_input` looks like a
        correction of the previous command, otherwise None. An empty string
        means a correction was detected but no new instruction was given.
        """
        lower_input = user_input.lower().strip()

        for marker in CORRECTION_MARKERS:
            if lower_input.startswith(marker):
                return user_input[len(marker):].strip(" ,.")

        if lower_input in ("no", "wrong", "that's wrong", "incorrect"):
            return ""

        return None

    def _route(self, user_input: str) -> str:
        """
        Classifies and dispatches a single instruction to the right handler.
        """

        classification = self.classifier.classify(
            user_input
        )

        clean_input = user_input.translate(str.maketrans("", "", string.punctuation))
        words = set(clean_input.lower().split())

        automation_intents = {"OPEN_APPLICATION", "SEARCH_WEB", "DESKTOP_AUTOMATION"}
        automation_keywords = {
            "close", "exit", "kill", "stop", "terminate", "open", "launch",
            "start", "run", "search", "google", "click", "type", "press",
            "move", "drag", "scroll", "find", "screenshot", "see", "show",
            "draw", "paint", "observe", "summarize", "view", "play", "youtube", "song", "music", "video"
        }
        is_automation = (classification.intent in automation_intents) or bool(words & automation_keywords)

        lower_input = user_input.lower().strip()

        # Check for requests to close/stop YouTube -- must be checked before
        # the "play on YouTube" match below, since both mention "youtube".
        close_verbs = {"close", "stop", "exit", "quit", "kill"}
        if "youtube" in lower_input and (words & close_verbs):
            hwnds = self.agent_loop.window_manager.find_windows("youtube")
            if not hwnds:
                return "I couldn't find any YouTube window open."
            closed = sum(
                1 for hwnd in hwnds
                if self.agent_loop.window_manager.close_window(hwnd)
            )
            return f"Closed {closed} YouTube window(s)." if closed else "Failed to close the YouTube window."

        # Check for direct YouTube song / video requests
        play_media_words = {"song", "songs", "music", "video", "videos", "track", "tracks", "audio"}
        if "youtube" in lower_input or ("play" in words and (words & play_media_words)):
            return self.agent_loop.browser.play_youtube(user_input)

        # Check for news / headlines requests -- fetch and summarize instead of
        # opening a browser search.
        news_keywords = {"news", "headlines", "headline"}
        if words & news_keywords:
            topic = None
            padded_input = f" {lower_input} "
            for marker in (" about ", " on ", " regarding ", " for "):
                if marker in padded_input:
                    candidate = padded_input.split(marker, 1)[1].strip().rstrip("?.! ")
                    if candidate and candidate not in ("today", "today's", "todays", "me"):
                        topic = candidate
                    break
            return self.news_service.summarize(topic)

        # Check for direct application opening requests (e.g. "microsoft edge", "open edge", "open chrome")
        app_launch_prefixes = ["open ", "launch ", "start ", "run "]
        target_app = lower_input
        for p in app_launch_prefixes:
            if target_app.startswith(p):
                target_app = target_app[len(p):].strip()

        registered_app = registry.get(target_app)
        if registered_app or target_app in ["edge", "microsoft edge", "msedge", "chrome", "google chrome", "notepad", "calculator", "calc", "paint", "vscode", "code", "word", "excel", "powerpoint", "spotify", "terminal", "cmd", "powershell", "explorer"]:
            app_key = registered_app.key if registered_app else target_app
            return self.agent_loop.app_manager.start_application(app_key)

        # Check for simple screen summary/observation queries
        screen_keywords = {"see", "summarize", "observe", "view", "what"}
        screen_indicators = {"screen", "desktop", "display", "monitor"}
        is_screen_query = bool(words & screen_keywords) and bool(words & screen_indicators)

        if is_screen_query:
            # Observe screen once and return description instantly
            obs = self.agent_loop.observer.observe()
            prompt = (
                f"The user asked: '{user_input}'.\n"
                f"Current Desktop Observation:\n{obs['summary_text']}\n"
                f"Please reply concisely and summarize exactly what is on the screen."
            )
            return self.provider.generate(
                system_prompt="You are JARVIS assisting the user by describing what is on their screen.",
                user_prompt=prompt
            )

        if not is_automation:
            # Handle conversational chats, memory settings, or standard queries
            return self.reasoning.resolve(
                user_input=user_input,
                classification=classification,
                provider=self.provider,
                memory=self.memory,
                tool_manager=self.tool_manager,
            )

        # --------------------------------------------------
        # Execute automation goals via the agent loop, which
        # already handles multi-step sequences internally.
        # --------------------------------------------------
        return self.agent_loop.run(user_input)
