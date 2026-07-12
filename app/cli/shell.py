"""
Interactive command shell.
"""

import os

from app.cli.router import CommandRouter
from app.brain.brain import Brain
from core.constants import APP_NAME, VERSION
from core.logger import log


class CommandShell:
    """
    Interactive command-line interface.
    """

    def __init__(self):

        self.router = CommandRouter()
        self.brain = Brain()

        self.router.register("help", self.help)
        self.router.register("version", self.version)
        self.router.register("status", self.status)
        self.router.register("clear", self.clear)
        self.router.register("hello", self.hello)

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