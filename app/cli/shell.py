"""
Interactive command shell.
"""

import os

from app.cli.router import CommandRouter
from app.brain.brain import Brain
from app.voice import VoiceController
from app.core.constants import APP_NAME, VERSION
from app.core.logger import log


class CommandShell:
    """
    Interactive command-line interface.
    """

    def __init__(self):

        self.router = CommandRouter()
        self.brain = Brain()
        self.voice = VoiceController(brain=self.brain)

        self.router.register("help", self.help)
        self.router.register("version", self.version)
        self.router.register("status", self.status)
        self.router.register("clear", self.clear)
        self.router.register("hello", self.hello)
        self.router.register("voice", self.voice_mode)
        self.router.register("listen", self.listen_command)
        self.router.register("speak", self.speak_command)
        self.router.register("wake", self.wake_command)
        self.router.register("wakeword", self.wake_command)



    def start(self):

        log.success("Command shell started.")

        while True:

            try:

                command = input("\njarvis > ").strip().lower()

                if not command:
                    continue

                if command == "exit":
                    log.info("Shutting down JARVIS...")
                    break

                if command in self.router.list_commands():
                    self.router.execute(command)
                else:
                    response = self.brain.think(command)
                    print(f"\nJARVIS > {response}")

            except KeyboardInterrupt:

                print()

                log.info("Shutdown requested.")

                break

    def help(self):

        print("\nAvailable Commands\n")

        for command in self.router.list_commands():
            print(command)

        print("exit")

    def version(self):

        print(f"{APP_NAME} {VERSION}")

    def status(self):

        log.success("All systems operational.")

    def clear(self):

        os.system("cls" if os.name == "nt" else "clear")

    def hello(self):

        print("Hello Mithun!")

    def voice_mode(self):
        """Starts continuous interactive voice loop."""
        self.voice.start_voice_loop()

    def listen_command(self):
        """Captures a single voice command from microphone."""
        self.voice.listen_and_process()

    def speak_command(self):
        """Test voice output."""
        self.voice.tts.speak("JARVIS voice system operational.")

    def wake_command(self):
        """Starts hands-free Wake Word activation mode ('Jarvis' or 'Hey Jarvis')."""
        self.voice.start_wake_word_mode()
