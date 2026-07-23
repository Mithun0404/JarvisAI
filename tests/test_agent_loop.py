"""
Unit tests for the Agent Loop Module.
"""

import json
import unittest
from unittest.mock import patch, MagicMock

from app.brain.agent_loop import AgentLoop, AGENT_LOOP_SYSTEM_PROMPT


class TestAgentLoop(unittest.TestCase):

    @patch("app.vision.observer.ScreenObserver.observe")
    def test_agent_loop_runs_to_finish(self, mock_observe):
        mock_provider = MagicMock()
        mock_memory = MagicMock()
        
        # Scenario: Step 1 decides to open paint, Step 2 decides to finish
        mock_observe.return_value = {
            "summary_text": "Notepad is visible.",
            "visible_windows": [],
            "detected_apps": []
        }
        
        step_responses = [
            '{"action": "open_app", "parameters": {"app_key": "paint"}, "thought": "I will open paint to fulfill the user input."}',
            '{"action": "finish", "parameters": {"response": "Goal reached!"}, "thought": "Paint is now open."}'
        ]
        mock_provider.chat.side_effect = step_responses

        loop = AgentLoop(mock_provider, mock_memory, max_steps=5)
        
        # Mock actual execution functions
        loop.app_manager = MagicMock()
        loop.app_manager.start_application.return_value = "Opening Paint..."

        response = loop.run("draw a picture")
        
        self.assertEqual(response, "Goal reached!")
        self.assertEqual(loop.app_manager.start_application.call_count, 1)
        loop.app_manager.start_application.assert_called_with("paint")

    @patch("app.vision.observer.ScreenObserver.observe")
    def test_agent_loop_json_recovery(self, mock_observe):
        mock_provider = MagicMock()
        mock_memory = MagicMock()

        mock_observe.return_value = {
            "summary_text": "Desktop is visible.",
            "visible_windows": [],
            "detected_apps": []
        }

        # Step 1: Bad JSON, Step 2: Valid JSON finish
        step_responses = [
            'Bad non-JSON format message from LLM',
            '{"action": "finish", "parameters": {"response": "Recovered!"}, "thought": "Task done."}'
        ]
        mock_provider.chat.side_effect = step_responses

        loop = AgentLoop(mock_provider, mock_memory, max_steps=5)
        response = loop.run("do something")
        
        self.assertEqual(response, "Recovered!")
        self.assertEqual(mock_provider.chat.call_count, 2)

    @patch("app.vision.observer.ScreenObserver.observe")
    def test_agent_loop_max_steps_exceeded(self, mock_observe):
        mock_provider = MagicMock()
        mock_memory = MagicMock()

        mock_observe.return_value = {
            "summary_text": "Desktop is visible.",
            "visible_windows": [],
            "detected_apps": []
        }

        # Continually decides to press enter
        mock_provider.chat.return_value = '{"action": "keyboard_press", "parameters": {"key": "enter"}, "thought": "Wait."}'

        loop = AgentLoop(mock_provider, mock_memory, max_steps=3)
        loop.keyboard = MagicMock()
        loop.keyboard.press.return_value = "Pressed enter."

        response = loop.run("press buttons")
        
        self.assertEqual(response, "Reached maximum step limit without achieving the goal.")
        self.assertEqual(loop.keyboard.press.call_count, 3)


if __name__ == "__main__":
    unittest.main()
