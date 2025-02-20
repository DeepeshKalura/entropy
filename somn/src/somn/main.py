from pynput import keyboard
import ollama
import queue
import sys
import sounddevice as sd
import soundfile as sf
from transformers import pipeline
import numpy as np
import threading
import time


class VoiceAssistant:
    def __init__(self):
        self.recording = False
        self.audio_queue = queue.Queue()
        self.sample_rate = 44100

        # Initialize models
        self.stt = pipeline("automatic-speech-recognition", model="openai/whisper-base")
        self.tts = pipeline("text-to-speech", model="hexgrad/Kokoro-82M")

        # Initialize Ollama
        self.llm = ollama.Client()

    def on_press(self, key):
        try:
            # Start recording with Alt + S
            if key == keyboard.Key.alt_l and hasattr(key, "char") and key.char == "s":
                if not self.recording:
                    self.start_recording()

            # Stop recording with Alt + D
            elif key == keyboard.Key.alt_l and hasattr(key, "char") and key.char == "d":
                if self.recording:
                    self.stop_recording()

            # Quit with Alt + Q
            elif key == keyboard.Key.alt_l and hasattr(key, "char") and key.char == "q":
                return False

        except AttributeError:
            pass
        return True

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Error: {status}")
        self.audio_queue.put(indata.copy())

    def start_recording(self):
        self.recording = True
        self.audio_data = []

        # Start recording stream
        self.stream = sd.InputStream(
            callback=self.audio_callback, channels=1, samplerate=self.sample_rate
        )
        self.stream.start()
        print("Recording started... Press Alt+D to stop")

    def stop_recording(self):
        self.recording = False
        self.stream.stop()
        self.stream.close()

        # Process recorded audio
        audio_data = np.concatenate([chunk for chunk in self.audio_queue.queue])
        sf.write("temp_recording.wav", audio_data, self.sample_rate)

        # Convert speech to text
        text = self.stt("temp_recording.wav")["text"]
        print(f"You said: {text}")

        # Get LLM response
        response = self.llm.chat(
            model="qwen:2.5", messages=[{"role": "user", "content": text}]
        )
        response_text = response["message"]["content"]
        print(f"Assistant: {response_text}")

        # Convert response to speech
        speech = self.tts(response_text)
        sf.write("response.wav", speech["audio"], speech["sampling_rate"])
        sd.play(speech["audio"], speech["sampling_rate"])
        sd.wait()


def main():
    assistant = VoiceAssistant()

    print("Voice Assistant started!")
    print("Controls:")
    print("Alt+S: Start recording")
    print("Alt+D: Stop recording and process")
    print("Alt+Q: Quit")

    with keyboard.Listener(on_press=assistant.on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
