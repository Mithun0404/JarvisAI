"""
Dynamic greeting generator for JARVIS.

Provides stylish, varied startup greetings customized by time of day
and speaks them using the voice controller.
"""

import random
from datetime import datetime
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

USER_NAME = "Mithun"

STYLISH_GREETING_TEMPLATES = [
    "{time_greeting} Boss. JARVIS online and all systems nominal. How can I help you today?",
    "{time_greeting} Boss. All core systems are online and operational. What can I help you with today?",
    "{time_greeting} Commander. JARVIS protocols active. What are we building today?",
    "Greetings, Boss. Systems fully synchronized. How may I be of service?",
    "{time_greeting} Captain. All neural modules are online. Tell me, what can I help you with right now?",
    "Hello Boss, JARVIS online and standing by. What project are we working on today?",
    "Welcome back Poindexter. Systems running at peak efficiency. How can I assist you today?",
    "{time_greeting} Commander. At your command—tell me, what would you like to accomplish today?",
]

STYLISH_FAREWELL_TEMPLATES = [
    "Goodbye Boss. Shutting down all core systems. Have a wonderful day!",
    "Deactivating neural protocols. Until next time Poindexter.",
    "JARVIS going offline. Powering down subroutines. Take care Boss.",
    "Goodbye {name}. All systems standing by until your return.",
    "Disconnecting neural links. Have a great rest of your day Boss.",
    "Shutting down primary modules. Goodbye {name}.",
]


def get_time_greeting() -> str:
    """Returns a greeting based on the current hour of the day."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 22:
        return "Good evening"
    else:
        return "Greetings"


def generate_stylish_greeting(name: str = USER_NAME) -> str:
    """Generates a stylish, dynamic greeting string."""
    time_greeting = get_time_greeting()
    template = random.choice(STYLISH_GREETING_TEMPLATES)
    return template.format(time_greeting=time_greeting, name=name)


def display_and_speak_greeting(voice_controller: Optional[object] = None, name: str = USER_NAME) -> str:
    """
    Renders a stylish greeting in the terminal and speaks it aloud via TTS.

    :param voice_controller: VoiceController instance for TTS.
    :param name: User name to greet.
    :return: The spoken greeting string.
    """
    greeting = generate_stylish_greeting(name=name)

    # Render terminal UI
    if HAS_RICH:
        console = Console()
        panel_content = Text()
        panel_content.append("JARVIS AI ASSISTANT\n", style="bold cyan")
        panel_content.append(f"> {greeting}", style="bold white")
        console.print(
            Panel(
                panel_content,
                border_style="bright_blue",
                padding=(1, 2),
                title="[bold blue]SYSTEM ONLINE[/bold blue]",
                title_align="left",
            )
        )
    else:
        print("\n" + "=" * 50)
        print(f"JARVIS > {greeting}")
        print("=" * 50 + "\n")

    # Speak greeting out loud via TTS
    if voice_controller and hasattr(voice_controller, "tts") and voice_controller.tts:
        voice_controller.tts.speak(greeting, async_speech=True)

    return greeting


def generate_stylish_farewell(name: str = USER_NAME) -> str:
    """Generates a stylish, dynamic farewell string."""
    template = random.choice(STYLISH_FAREWELL_TEMPLATES)
    return template.format(name=name)


def display_and_speak_farewell(voice_controller: Optional[object] = None, name: str = USER_NAME) -> str:
    """
    Renders a stylish farewell message in the terminal and speaks it aloud via TTS during shutdown.

    :param voice_controller: VoiceController instance for TTS.
    :param name: User name to greet.
    :return: The spoken farewell string.
    """
    farewell = generate_stylish_farewell(name=name)

    # Render terminal UI
    if HAS_RICH:
        console = Console()
        panel_content = Text()
        panel_content.append("JARVIS AI ASSISTANT\n", style="bold red")
        panel_content.append(f"> {farewell}", style="bold white")
        console.print(
            Panel(
                panel_content,
                border_style="red",
                padding=(1, 2),
                title="[bold red]SYSTEM SHUTDOWN[/bold red]",
                title_align="left",
            )
        )
    else:
        print("\n" + "=" * 50)
        print(f"JARVIS > {farewell}")
        print("=" * 50 + "\n")

    # Speak farewell synchronously so speech finishes before process exits
    if voice_controller and hasattr(voice_controller, "tts") and voice_controller.tts:
        voice_controller.tts.speak(farewell, async_speech=False)

    return farewell
