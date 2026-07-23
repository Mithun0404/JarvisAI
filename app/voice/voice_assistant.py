"""
Voice Assistant Controller for JARVIS.

Coordinates Speech-To-Text input, Brain processing, and Text-To-Speech response output.
"""

from typing import Optional
from loguru import logger

from app.voice.tts import TextToSpeech
from app.voice.stt import SpeechToText
from app.voice.wake_word import WakeWordDetector


class VoiceController:
    """
    Manages interactive voice interaction loops, wake word detection, and single voice commands.
    """

    def __init__(self, brain=None) -> None:
        """
        Initialize VoiceController with optional Brain instance.
        """
        self.brain = brain
        self.tts = TextToSpeech()
        self.stt = SpeechToText()
        self.wake_detector = WakeWordDetector()


    def set_brain(self, brain) -> None:
        """Set or update the Brain instance."""
        self.brain = brain

    def listen_and_process(self, timeout: float = 6.0) -> Optional[str]:
        """
        Captures one voice command, passes it to Brain, and speaks out the result.
        
        :return: Response string if command was captured & processed, None otherwise.
        """
        if not self.brain:
            err_msg = "Brain is not initialized in VoiceController."
            logger.error(err_msg)
            self.tts.speak(err_msg)
            return None

        self.tts.speak("Listening...", async_speech=False)
        user_speech = self.stt.listen(timeout=timeout)

        if not user_speech:
            self.tts.speak("I didn't hear any command.")
            return None

        print(f"\n[Voice Input]: {user_speech}")
        self.tts.speak(f"Processing command: {user_speech}")

        try:
            response = self.brain.think(user_speech)
            if response:
                print(f"\nJARVIS > {response}")
                # Speak response out loud
                self.tts.speak(response)
            return response
        except Exception as e:
            error_text = f"An error occurred while processing your voice command: {e}"
            logger.error(error_text)
            self.tts.speak("Sorry, an error occurred while processing your request.")
            return None

    def start_voice_loop(self) -> None:
        """
        Runs an interactive voice command loop. Continues until user says 'exit', 'quit', or 'stop'.
        """
        self.tts.speak("Voice mode activated. Speak your command.")
        logger.info("Started continuous voice command mode.")

        exit_keywords = {"exit", "quit", "stop", "cancel", "bye", "shutdown"}

        while True:
            try:
                print("\n[Voice Mode Active - Listening...]")
                command = self.stt.listen(timeout=8.0, phrase_time_limit=12.0)

                if not command:
                    continue

                clean_cmd = command.strip().lower()
                print(f"\n[Voice Input]: {command}")

                if clean_cmd in exit_keywords:
                    self.tts.speak("Exiting voice mode. Returning to standard shell.")
                    print("\n[Exiting Voice Mode]")
                    break

                self.tts.speak(f"Got it: {command}")
                
                if self.brain:
                    response = self.brain.think(command)
                    if response:
                        print(f"\nJARVIS > {response}")
                        self.tts.speak(response)

            except KeyboardInterrupt:
                self.tts.speak("Voice mode cancelled.")
                break
            except Exception as err:
                logger.error(f"Voice loop error: {err}")
                self.tts.speak("Error in voice loop. Resuming...")

    def start_wake_word_mode(self) -> None:
        """
        Runs continuous background wake word listening.
        Wakes up when user says "Jarvis" or "Hey Jarvis".
        """
        self.tts.speak("Wake word mode online. Say 'Jarvis' or 'Hey Jarvis' to wake me up.")
        print("\n[Passive Listening - Say 'Jarvis' or 'Hey Jarvis' | Press Ctrl+C to exit]")
        logger.info("Started wake word detection mode.")

        while True:
            try:
                is_woken, inline_cmd = self.wake_detector.listen_for_wake_word(timeout=3.0)

                if is_woken:
                    print("\n⚡ [WAKE WORD DETECTED] ⚡")
                    
                    if inline_cmd:
                        command = inline_cmd
                        self.tts.speak(f"Yes, Mithun? Processing {command}")
                    else:
                        self.tts.speak("Yes, Mithun? I am listening.")
                        print("[Listening for command...]")
                        command = self.stt.listen(timeout=6.0, phrase_time_limit=10.0)

                    if command:
                        print(f"\n[Voice Input]: {command}")
                        if self.brain:
                            response = self.brain.think(command)
                            if response:
                                print(f"\nJARVIS > {response}")
                                self.tts.speak(response)
                    else:
                        self.tts.speak("I didn't hear a command. Standing by.")

                    print("\n[Resuming Wake Word Listening...]")

            except KeyboardInterrupt:
                self.tts.speak("Wake word mode stopped.")
                print("\n[Wake Word Mode Stopped]")
                break
            except Exception as err:
                logger.error(f"Wake word error: {err}")

