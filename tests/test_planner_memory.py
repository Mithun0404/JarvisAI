"""
Unit tests for Goal Planner and Memory manager capabilities.
"""

import json
import unittest
from unittest.mock import patch, MagicMock

from app.planner.planner import TaskPlanner
from app.memory.manager import MemoryManager


class TestGoalPlanner(unittest.TestCase):

    @patch("app.brain.providers.ollama_provider.OllamaProvider.generate")
    def test_decomposes_goals_to_subgoals(self, mock_gen):
        mock_gen.return_value = json.dumps({
            "actions": [
                {"intent": "SUBGOAL", "parameters": {"goal": "Open Chrome and search weather"}},
                {"intent": "SUBGOAL", "parameters": {"goal": "Open Notepad and type result"}}
            ]
        })

        planner = TaskPlanner()
        plan = planner.create_plan("what is weather and then save it in notepad")
        
        self.assertEqual(len(plan.actions), 2)
        self.assertEqual(plan.actions[0].intent, "SUBGOAL")
        self.assertEqual(plan.actions[0].parameters["goal"], "Open Chrome and search weather")
        self.assertEqual(plan.actions[1].parameters["goal"], "Open Notepad and type result")


class TestMemoryManagerExtensions(unittest.TestCase):

    def test_preference_storage(self):
        # Mock LongTermMemory persistence
        provider = MagicMock()
        manager = MemoryManager(provider)
        
        manager.remember_preference("color", "blue")
        pref = manager.get_preference("color")
        self.assertEqual(pref, "blue")

    def test_workflow_storage(self):
        provider = MagicMock()
        manager = MemoryManager(provider)
        
        workflow_steps = ["open_chrome", "type_url", "drag_mouse"]
        manager.remember_workflow("search_job", workflow_steps)
        
        retrieved = manager.get_workflow("search_job")
        self.assertEqual(retrieved, workflow_steps)

    def test_observation_storage(self):
        provider = MagicMock()
        manager = MemoryManager(provider)
        
        # Verify observation pushes into SessionMemory
        manager.add_observation("Chrome is active on page.")
        msgs = manager.conversation()
        self.assertEqual(len(msgs), 1)
        self.assertEqual(msgs[0]["role"], "observation")
        self.assertEqual(msgs[0]["content"], "Chrome is active on page.")


if __name__ == "__main__":
    unittest.main()
