"""
Agent Loop Module.

Executes autonomous loop processing: Observe -> Reason -> Decide -> Execute -> Repeat.
"""

import json
from typing import Dict, Any, List, Optional
from loguru import logger

from app.automation.mouse import MouseController
from app.automation.keyboard import KeyboardController
from app.automation.clipboard import ClipboardController
from app.automation.window_manager import WindowManager
from app.automation.app_manager import ApplicationManager
from app.automation.browser_controller import BrowserController
from app.vision.observer import ScreenObserver


AGENT_LOOP_SYSTEM_PROMPT = """
You are JARVIS, an autonomous AI computer operator running on Windows.
Your goal is to satisfy the user's instructions through a sequence of actions.

You have access to:
1. Low-level Desktop Controls: mouse moves, clicks, keyboard typing, hotkeys, and clipboard actions.
2. Window & Process Controls: launch apps, close apps, resize/maximize/minimize/focus windows.
3. Browser Controls: open page, search web, browser scrolling, and tab control.
4. Screen Observation: list of visible windows with titles and layout details.

Observations format:
The current state of your screen will be described to you. Pay close attention to what windows are active and focused.
Specifically, check the "detected_apps" list. If an application (e.g., 'chrome') is NOT present in "detected_apps", it is NOT running. Do NOT confuse file names or window titles of other programs (like VS Code showing code files titled 'test_browser.py' or 'chrome_test.py') with the target application itself. If the app is not in the detected_apps list, you can assume it has been successfully closed.

You MUST output your decision in EXACTLY this JSON structure. Do not output markdown code blocks (e.g. ```json), do not explain, just return raw JSON:
{
    "action": "<action_name>",
    "parameters": { ... },
    "thought": "<your short reasoning before taking this action>"
}

Supported Actions:
- open_app: {"app_key": "notepad" | "chrome" | "vscode" | "paint" | "calc" | "cmd" | "powershell" | "explorer"}
- close_app: {"app_key": "notepad" | "chrome" | "vscode" | etc.}
- focus_window: {"hwnd": <window_handle_integer>}
- resize_window: {"hwnd": <window_handle_integer>, "width": <int>, "height": <int>}
- move_window: {"hwnd": <window_handle_integer>, "x": <int>, "y": <int>}
- minimize_window: {"hwnd": <window_handle_integer>}
- maximize_window: {"hwnd": <window_handle_integer>}
- close_window: {"hwnd": <window_handle_integer>}
- mouse_move: {"x": <int>, "y": <int>}
- mouse_click: {}
- mouse_double_click: {}
- mouse_right_click: {}
- mouse_drag_between: {"start_x": <int>, "start_y": <int>, "end_x": <int>, "end_y": <int>}
- keyboard_type: {"text": "<text_to_type>"}
- keyboard_press: {"key": "<key_name>"}
- keyboard_hotkey: {"keys": ["ctrl", "c"]}
- clipboard_set: {"text": "<text_to_copy>"}
- clipboard_get: {}
- browser_open_url: {"url": "<url>"}
- browser_search: {"query": "<query>"}
- browser_scroll: {"direction": "down" | "up", "amount": <int>}
- browser_new_tab: {}
- browser_close_tab: {}
- browser_go_back: {}
- browser_go_forward: {}
- finish: {"response": "<final summary statement to the user>"}

Examples:
- To close chrome, choose action `close_app` with parameters `{"app_key": "chrome"}`.
- To type something, run `keyboard_type` with parameters `{"text": "my text"}`.
- If the current screen state indicates you have achieved the goal, choose action `finish` with parameters `{"response": "Successfully closed Chrome."}`.
"""


class AgentLoop:
    """
    Core engine that coordinates the agent's actions iteratively.
    """

    def __init__(self, provider, memory, max_steps: int = 12) -> None:
        self.provider = provider
        self.memory = memory
        self.max_steps = max_steps

        # Controllers
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.clipboard = ClipboardController()
        self.window_manager = WindowManager()
        self.app_manager = ApplicationManager()
        self.browser = BrowserController()
        self.observer = ScreenObserver()

    def run(self, goal: str) -> str:
        """
        Runs the loop until goal is achieved or max_steps is hit.
        """
        logger.info(f"Starting Agent Loop for goal: '{goal}'")
        
        # Build initial messages list
        messages = [
            {"role": "system", "content": AGENT_LOOP_SYSTEM_PROMPT},
            {"role": "user", "content": f"User Goal: {goal}"}
        ]

        step = 0
        while step < self.max_steps:
            step += 1
            logger.debug(f"--- Agent Loop Step {step} ---")

            # 1. Observe
            observation = self.observer.observe()
            obs_text = observation["summary_text"]
            logger.debug(f"Observation Summary:\n{obs_text}")

            # Append current observation
            messages.append({"role": "user", "content": f"Current Observation:\n\n{obs_text}\n\nWhat is the next action?"})

            # 2. Reason & Decide
            response_raw = self.provider.chat(messages)
            logger.debug(f"LLM Raw Decision Response: {response_raw}")

            # Bulletproof JSON extraction from the LLM outputs
            clean_json = response_raw.strip()
            start_idx = clean_json.find("{")
            end_idx = clean_json.rfind("}")
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                clean_json = clean_json[start_idx : end_idx + 1]

            try:
                decision = json.loads(clean_json)
            except Exception as e:
                logger.warning(f"Failed to parse LLM JSON: {e}. Retrying with warning.")
                messages.append({
                    "role": "user",
                    "content": f"Error: Your response was not valid JSON. Please reply with ONLY the JSON object format described."
                })
                continue

            action = decision.get("action", "").lower()
            params = decision.get("parameters", {})
            thought = decision.get("thought", "")

            logger.success(f"Action Decide: {action.upper()} | Thought: {thought}")

            # Keep execution trace in LLM message history
            messages.append({"role": "assistant", "content": clean_json})

            # Check if finished
            if action == "finish":
                response = params.get("response", "Task completed.")
                logger.success(f"Agent Loop completed successfully: {response}")
                return response

            # 3. Execute
            exec_result = self._execute_action(action, params)
            logger.debug(f"Execution Result: {exec_result}")

            # Record result
            messages.append({"role": "user", "content": f"Execution Result: {exec_result}"})

        return "Reached maximum step limit without achieving the goal."

    def _execute_action(self, action: str, params: Dict[str, Any]) -> str:
        """
        Maps action names to the controller handlers.
        """
        try:
            # Application lifecycle
            if action == "open_app":
                return self.app_manager.start_application(params.get("app_key", ""))
            elif action == "close_app":
                return self.app_manager.close_application(params.get("app_key", ""))

            # Window management
            elif action == "focus_window":
                hwnd = int(params.get("hwnd", 0))
                ok = self.window_manager.focus_window(hwnd)
                return "Successfully focused window" if ok else "Failed to focus window"
            elif action == "resize_window":
                hwnd = int(params.get("hwnd", 0))
                w = int(params.get("width", 0))
                h = int(params.get("height", 0))
                ok = self.window_manager.resize_window(hwnd, w, h)
                return "Resized window" if ok else "Failed to resize window"
            elif action == "move_window":
                hwnd = int(params.get("hwnd", 0))
                x = int(params.get("x", 0))
                y = int(params.get("y", 0))
                ok = self.window_manager.move_window(hwnd, x, y)
                return "Moved window" if ok else "Failed to move window"
            elif action == "maximize_window":
                hwnd = int(params.get("hwnd", 0))
                ok = self.window_manager.maximize_window(hwnd)
                return "Maximized window" if ok else "Failed to maximize window"
            elif action == "minimize_window":
                hwnd = int(params.get("hwnd", 0))
                ok = self.window_manager.minimize_window(hwnd)
                return "Minimized window" if ok else "Failed to minimize window"
            elif action == "close_window":
                hwnd = int(params.get("hwnd", 0))
                ok = self.window_manager.close_window(hwnd)
                return "Gracefully sent close window message" if ok else "Failed to close window"

            # Mouse controller
            elif action == "mouse_move":
                return self.mouse.move(int(params.get("x", 0)), int(params.get("y", 0)))
            elif action == "mouse_click":
                return self.mouse.click()
            elif action == "mouse_double_click":
                return self.mouse.double_click()
            elif action == "mouse_right_click":
                return self.mouse.right_click()
            elif action == "mouse_drag_between":
                self.mouse.move(int(params.get("start_x", 0)), int(params.get("start_y", 0)))
                return self.mouse.drag_to(int(params.get("end_x", 0)), int(params.get("end_y", 0)))

            # Keyboard controller
            elif action == "keyboard_type":
                return self.keyboard.type_text(params.get("text", ""))
            elif action == "keyboard_press":
                return self.keyboard.press(params.get("key", ""))
            elif action == "keyboard_hotkey":
                return self.keyboard.hotkey(*params.get("keys", []))

            # Clipboard controller
            elif action == "clipboard_set":
                ok = self.clipboard.set_text(params.get("text", ""))
                return "Set clipboard data" if ok else "Failed to write to clipboard"
            elif action == "clipboard_get":
                val = self.clipboard.get_text()
                return f"Clipboard text is: '{val}'"

            # Browser controller
            elif action == "browser_open_url":
                return self.browser.open_url(params.get("url", ""))
            elif action == "browser_search":
                return self.browser.search(params.get("query", ""))
            elif action == "browser_scroll":
                return self.browser.scroll(params.get("direction", "down"), int(params.get("amount", 2)))
            elif action == "browser_new_tab":
                return self.browser.new_tab()
            elif action == "browser_close_tab":
                return self.browser.close_tab()
            elif action == "browser_go_back":
                return self.browser.go_back()
            elif action == "browser_go_forward":
                return self.browser.go_forward()

            else:
                return f"Unknown or unmapped action: '{action}'."
        except Exception as err:
            return f"Action execution threw error: {err}"
