import sys
import os
import json
import time
import keyboard
import threading
from voxpolish.core.audio import AudioCollector
from voxpolish.core.stt import WhisperSTT

# Ensure the app root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class VoxPolishApp:
    """
    Main orchestration class for VoxPolish.
    Handles hotkeys, audio capture, and text injection.
    """
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.hotkey = self.config.get("hotkey", "ctrl+alt+z")
        
        # Core components
        self.collector = AudioCollector()
        self.stt = WhisperSTT() # Model pre-load here
        
        self.is_recording = False
        self.lock = threading.Lock()

    def _load_config(self):
        """Loads configuration from JSON file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
        
        # Create default config
        default_config = {"hotkey": "ctrl+alt+z"}
        try:
            with open(self.config_file, "w") as f:
                json.dump(default_config, f, indent=4)
        except Exception as e:
            print(f"Error saving default config: {e}")
        return default_config

    def _on_hotkey_toggle(self):
        """Hotkey callback: toggles recording and triggers STT on stop."""
        with self.lock:
            if not self.is_recording:
                # Start recording
                self.is_recording = True
                self.collector.start()
                print(f"--- LISTENING (Press {self.hotkey} to stop) ---", flush=True)
            else:
                # Stop recording
                self.is_recording = False
                self.collector.stop()
                print("--- STOPPED (Processing...) ---", flush=True)
                
                # Perform STT and injection asynchronously
                threading.Thread(target=self._process_and_inject).start()

    def _process_and_inject(self):
        """Extracts captured audio, transcribes, and injects text."""
        try:
            # 1. Get raw speech from collector
            audio_data = self.collector.get_captured_audio()
            if len(audio_data) == 0:
                print("No speech detected.")
                return
                
            # 2. Transcribe using Faster-Whisper
            start_time = time.time()
            text = self.stt.transcribe(audio_data)
            duration = time.time() - start_time
            print(f"Transcription ({duration:.2f}s): {text}", flush=True)
            
            # 3. Inject text via global keyboard (simulate typing)
            if text:
                # injector: insert text at current cursor
                keyboard.write(text)
                print("Successfully injected text into active window.", flush=True)
            
        except Exception as e:
            print(f"Error in processing: {e}", flush=True)

    def run(self):
        """Main event loop."""
        print(f"--- VoxPolish Started ---", flush=True)
        print(f"Global Hotkey: {self.hotkey}", flush=True)
        
        # Register the hotkey
        keyboard.add_hotkey(self.hotkey, self._on_hotkey_toggle)
        
        print("Waiting for your command... (Press Esc to quit the app)", flush=True)
        keyboard.wait('esc') # Keep the app running until Esc is pressed
        print("VoxPolish exiting...")

if __name__ == "__main__":
    app = VoxPolishApp()
    app.run()
