"""
Interactive command shell.
"""

import os

from app.cli.router import CommandRouter
from app.brain.brain import Brain
from app.voice import VoiceController
from app.core.constants import APP_NAME, VERSION
from app.core.logger import log
from app.core.greetings import display_and_speak_greeting, display_and_speak_farewell


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
        self.router.register("voices", self.list_voices)
        self.router.register("josh", self.activate_josh_mode)

    def start(self):

        log.success("Command shell started.")
        # Stylish dynamic greeting spoken in neural voice
        display_and_speak_greeting(self.voice)

        while True:

            try:

                raw_input = input("\njarvis > ").strip()

                if not raw_input:
                    continue

                parts = raw_input.split(maxsplit=1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                if cmd == "exit":
                    log.info("Shutting down JARVIS...")
                    display_and_speak_farewell(self.voice)
                    break

                if cmd in ("setvoice", "voice-set"):
                    self.change_voice(args)
                elif cmd in ("setrate", "voice-rate"):
                    self.change_rate(args)
                elif cmd in ("setpitch", "voice-pitch"):
                    self.change_pitch(args)
                elif cmd in ("setpause", "pause-threshold"):
                    self.change_pause(args)
                elif cmd in self.router.list_commands():
                    self.router.execute(cmd)
                else:
                    response = self.brain.think(raw_input)
                    print(f"\nJARVIS > {response}")
                    if response:
                        self.voice.tts.speak(response)

            except KeyboardInterrupt:

                print()
                log.info("Shutdown requested.")
                display_and_speak_farewell(self.voice)
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
        display_and_speak_greeting(self.voice)

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

    def list_voices(self):
        """Display available high-clarity voice presets."""
        print("\n--- Available Neural Voice Presets ---")
        voices = self.voice.tts.get_available_voices()
        for key, name in voices.items():
            print(f"  • {key:<12} -> {name}")
        print("\nUse 'setvoice <preset_or_name>' to switch voice.")
        print("Example: setvoice aria | setvoice jarvis | setvoice sonia\n")

    def change_voice(self, voice_arg: str):
        """Change the active TTS voice dynamically."""
        if not voice_arg:
            print("Usage: setvoice <voice_key_or_name> (e.g. setvoice aria or setvoice jarvis)")
            return
        self.voice.tts.set_voice(voice_arg)
        msg = f"Voice updated to {self.voice.tts.voice}."
        print(f"\n[JARVIS]: {msg}")
        self.voice.tts.speak(msg)

    def change_rate(self, rate_arg: str):
        """Change TTS speech speed percentage (e.g. 0 for normal, 10 for faster, -10 for slower)."""
        try:
            rate_val = int(rate_arg)
            self.voice.tts.set_speech_rate(rate_val)
            msg = f"Speech speed set to {self.voice.tts.speech_rate}."
            print(f"\n[JARVIS]: {msg}")
            self.voice.tts.speak(msg)
        except ValueError:
            print("Usage: setrate <percentage_int> (e.g., setrate 0 for normal clarity, setrate 10 for +10%)")

    def change_pitch(self, pitch_arg: str):
        """Change TTS pitch modifier in Hz (e.g. 3 for +3Hz, -2 for -2Hz)."""
        try:
            pitch_val = int(pitch_arg)
            self.voice.tts.set_pitch(pitch_val)
            msg = f"Pitch set to {self.voice.tts.speech_pitch}."
            print(f"\n[JARVIS]: {msg}")
            self.voice.tts.speak(msg)
        except ValueError:
            print("Usage: setpitch <hz_int> (e.g., setpitch 3 for vibrant pitch lift)")

    def activate_josh_mode(self):
        """Activates high-energy, passionate Josh speaker mode."""
        self.voice.tts.enable_josh_mode("josh")
        msg = "Josh mode activated! All systems operating with maximum passion, high energy, and dynamic pitch."
        print(f"\n⚡ [JARVIS JOSH MODE]: {msg}")
        self.voice.tts.speak("Josh mode activated! Standing by with high energy.")

    def change_pause(self, pause_arg: str):
        """Change STT listening silence pause threshold (e.g. setpause 5 for 5 seconds pause)."""
        try:
            val = float(pause_arg)
            self.voice.stt.set_pause_threshold(val)
            msg = f"Listening silence pause threshold set to {self.voice.stt.recognizer.pause_threshold} seconds."
            print(f"\n[JARVIS]: {msg}")
            self.voice.tts.speak(msg)
        except ValueError:
            print("Usage: setpause <seconds> (e.g. setpause 5 for 5 seconds silence pause after speaking)")


