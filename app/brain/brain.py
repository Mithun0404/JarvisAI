"""
Brain module.
"""

from app.brain.classifier import IntentClassifier
from app.brain.providers.ollama_provider import OllamaProvider
from app.brain.reasoning import ReasoningEngine
from app.brain.agent_loop import AgentLoop
from app.memory.manager import MemoryManager
from app.tools.manager import ToolManager


class Brain:

    def __init__(self):
        from app.planner import TaskPlanner, TaskExecutor

        self.provider = OllamaProvider()

        self.memory = MemoryManager(
            self.provider
        )

        self.tool_manager = ToolManager()

        self.reasoning = ReasoningEngine()

        self.classifier = IntentClassifier(
            self.provider
        )

        self.planner = TaskPlanner(
            self.provider
        )

        self.executor = TaskExecutor()  

        self.agent_loop = AgentLoop(
            self.provider,
            self.memory
        )

    def think(self, user_input: str):

        self.memory.add_user(user_input)

        # --------------------------------------------------
        # General Conversation Intent
        # --------------------------------------------------
        classification = self.classifier.classify(
            user_input
        )

        import string
        clean_input = user_input.translate(str.maketrans("", "", string.punctuation))
        words = set(clean_input.lower().split())

        automation_intents = {"OPEN_APPLICATION", "SEARCH_WEB", "DESKTOP_AUTOMATION"}
        automation_keywords = {
            "close", "exit", "kill", "stop", "terminate", "open", "launch", 
            "start", "run", "search", "google", "click", "type", "press", 
            "move", "drag", "scroll", "find", "screenshot", "see", "show",
            "draw", "paint", "observe", "summarize", "view"
        }
        is_automation = (classification.intent in automation_intents) or bool(words & automation_keywords)

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
            response = self.provider.generate(
                system_prompt="You are JARVIS assisting the user by describing what is on their screen.",
                user_prompt=prompt
            )
        elif not is_automation:
            # Handle conversational chats, memory settings, or standard queries
            response = self.reasoning.resolve(
                user_input=user_input,
                classification=classification,
                provider=self.provider,
                memory=self.memory,
                tool_manager=self.tool_manager,
            )
        else:
            # --------------------------------------------------
            # Decompose and execute complex goals
            # --------------------------------------------------
            plan = self.planner.create_plan(user_input)
            
            if len(plan.actions) > 1:
                results = []
                for action in plan.actions:
                    subgoal = action.parameters.get("goal")
                    if subgoal:
                        res = self.agent_loop.run(subgoal)
                        results.append(f"Subgoal Result [{subgoal}]: {res}")
                response = "\n".join(results)
            else:
                # Direct execute for single/simple goals
                response = self.agent_loop.run(user_input)

        self.memory.add_assistant(response)

        return response