import sys
import os
import json
import time
import keyboard
import threading
import traceback
from dotenv import load_dotenv
from voxpolish.core.audio import AudioCollector
from voxpolish.core.stt import NvidiaSTT
from voxpolish.core.wake import WakeWordListener

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal
from voxpolish.ui.wedge import VoxWedgeUI
from voxpolish.core.data import data_manager

import time

# 1. CRITICAL: DLL Search Path for Windows (PyInstaller)
if getattr(sys, 'frozen', False):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    # Add root and _internal to the DLL search path
    if hasattr(os, 'add_dll_directory'):
        os.add_dll_directory(base_path)
        internal_dlls = os.path.join(base_path, "_internal")
        if os.path.exists(internal_dlls):
            os.add_dll_directory(internal_dlls)

def crash_report(e):
    try:
        # Write to the SAME folder as the .exe
        exe_dir = os.path.dirname(sys.executable)
        report_path = os.path.join(exe_dir, "crash_report.txt")
        with open(report_path, "w") as f:
            f.write(f"CRASH REPORT - {time.ctime()}\n")
            f.write("-" * 30 + "\n")
            f.write(str(e) + "\n")
            traceback.print_exc(file=f)
        print(f"CRITICAL ERROR: {e}. Report saved to {report_path}", flush=True)
    except:
        pass

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        
        # In a 'onedir' build, assets are often moved to the _internal folder
        internal_path = os.path.join(base_path, "_internal", relative_path)
        if os.path.exists(internal_path):
            return internal_path
            
        return os.path.join(base_path, relative_path)
    except Exception:
        return os.path.join(os.path.abspath("."), relative_path)

# Load .env for API Credentials
load_dotenv()

class VoxWorker(QObject):
    """
    Background worker that handles transcription loop.
    Emits status changes to the UI.
    """
    status_changed = pyqtSignal(str) # ['ready', 'listening', 'polishing', 'done', 'error']
    transcription_ready = pyqtSignal(str, str) # text, mode

    def __init__(self, stt, audio_collector, wake_listener):
        super().__init__()
        self.stt = stt
        self.audio_collector = audio_collector
        self.wake_listener = wake_listener
        
        # Config
        self.config = self._load_config()
        self.hotkey = self.config.get("hotkey", "ctrl+alt+z")
        self.coding_hotkey = self.config.get("coding_hotkey", "ctrl+alt+c")
        self.wake_word_enabled = self.config.get("wake_word_enabled", True)
        
        # State
        self.is_recording = False
        self.current_mode = "standard" # "standard" or "coding"

    def _load_config(self):
        config_file = "config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "hotkey": "ctrl+alt+z",
            "coding_hotkey": "ctrl+alt+c",
            "wake_word_enabled": True
        }

    def run(self):
        """Main loop started in a separate thread."""
        print(f"VoxPolish Worker started. Hotkeys: {self.hotkey}, {self.coding_hotkey}", flush=True)
        
        # 1. Setup Hotkeys
        keyboard.add_hotkey(self.hotkey, lambda: self.toggle_recording("standard"))
        keyboard.add_hotkey(self.coding_hotkey, lambda: self.toggle_recording("coding"))
        
        # 2. Start Wake Word Loop (if enabled)
        if self.wake_word_enabled and self.wake_listener:
            threading.Thread(target=self._wake_word_loop, daemon=True).start()
            
        # Keep thread alive
        while True:
            time.sleep(1)

    def _wake_word_loop(self):
        """Background loop for wake word detection. Processes every chunk sequentially."""
        print("Wake Word detection active...", flush=True)
        while True:
            if not self.is_recording:
                # Use the new blocking getter to ensure we don't miss any audio data
                chunk = self.audio_collector.get_next_wake_chunk()
                if chunk is not None and len(chunk) > 0:
                    if self.wake_listener.predict(chunk):
                        # Use a small delay after detection to avoid double triggers
                        # and allow the toggle to complete
                        self.toggle_recording("standard")
                        time.sleep(1.0) 
            else:
                # DRAIN the wake queue while recording so we don't process 
                # minutes of old audio when we stop recording
                while not self.audio_collector.wake_queue.empty():
                    self.audio_collector.wake_queue.get_nowait()
                time.sleep(0.1)

    def toggle_recording(self, mode):
        """Starts or stops the recording process."""
        self.current_mode = mode
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        print(f"Recording started ({self.current_mode})...", flush=True)
        self.is_recording = True
        self.status_changed.emit("listening")
        self.audio_collector.start()
        
        # Start auto-stop monitoring thread
        threading.Thread(target=self._monitor_silence, daemon=True).start()

    def _monitor_silence(self):
        """Background thread to detect end-of-speech silence."""
        silence_threshold = 1.4  # seconds of silence before auto-stop
        max_silence_chunks = int(silence_threshold / 0.03) # 30ms frames
        silence_counter = 0
        
        # Initial grace period (allow time to start talking)
        time.sleep(1.0)
        
        while self.is_recording:
            chunk = self.audio_collector.get_latest_chunk()
            if chunk is not None and not self.audio_collector.is_speech(chunk):
                silence_counter += 1
            else:
                silence_counter = 0 # Reset on any speech
                
            if silence_counter >= max_silence_chunks:
                print("Auto-Endpoint: Silence detected.", flush=True)
                self.stop_recording()
                break
            time.sleep(0.03)

    def stop_recording(self):
        print("Recording stopped. Polishing...", flush=True)
        self.is_recording = False
        self.status_changed.emit("processing")
        
        raw_audio = self.audio_collector.stop()
        
        # Start transcription thread to not block hotkey cleanup
        threading.Thread(target=self._process_audio, args=(raw_audio,)).start()

    def _process_audio(self, raw_audio):
        try:
            # 1. STT
            text = self.stt.transcribe(raw_audio)
            if not text or len(text.strip()) < 2:
                print("No clear speech detected.")
                return

            # Clean transcribed text (remove extra spaces/newlines)
            output_text = text.strip().replace("\n", " ").replace("\r", "")
            print(f"Final output: {output_text}")
            
            # 2. Output (Paste)
            keyboard.write(output_text)
            
            # 3. Save to History
            data_manager.add_history(output_text, self.current_mode)
            
            # 4. Notify UI
            self.transcription_ready.emit(output_text, self.current_mode)
            self.status_changed.emit("success")
            
        except Exception as e:
            print(f"Error in processing: {e}")
            self.status_changed.emit("error")
        finally:
            # Always return to ready after a tiny delay
            time.sleep(0.5)
            self.status_changed.emit("ready")

def main():
    try:
        app = QApplication(sys.argv)
        
        # Initialize Core Components
        print("Initializing Core Components...", flush=True)
        stt = NvidiaSTT()
        
        # Load configuration for wake words
        try:
            with open("config.json", "r") as f:
                config_data = json.load(f)
            wake_words = config_data.get("wake_words", ["alexa"])
            wake_threshold = config_data.get("wake_threshold", 0.5)
        except Exception:
            wake_words = ["alexa"]
            wake_threshold = 0.5
            
        collector = AudioCollector()
        collector.start_stream() # MANDATORY START HARDWARE
        
        # Setup Wake Word with config words
        wake = None
        try:
            print(f"Initializing Wake Word Engine with {wake_words} (Threshold: {wake_threshold})...", flush=True)
            wake = WakeWordListener(model_names=wake_words, threshold=wake_threshold)
        except Exception as e:
            print(f"Wake Word Engine failed to start: {e}. Voice activation disabled.", flush=True)
        
        # Setup UI
        window = VoxWedgeUI()
        window.show()
        
        # Setup Worker
        worker = VoxWorker(stt, collector, wake)
        worker_thread = QThread()
        worker.moveToThread(worker_thread)
        
        # Connect signals
        worker.status_changed.connect(window.update_state)
        # We need a slot for transcription_ready if we want to show it in UI
        
        worker_thread.started.connect(worker.run)
        worker_thread.start()
        
        print("Application ready.", flush=True)
        sys.exit(app.exec())
    except Exception as e:
        crash_report(e)
        print(f"\nCRITICAL ERROR: {e}", flush=True)
        import traceback
        traceback.print_exc()
        # Keep console open in EXE mode
        if getattr(sys, 'frozen', False):
            print("\n" + "="*40)
            print("APPLICATION CRASHED. Detailed report might be in crash_report.txt.")
            print("="*40)
            input("\nPress Enter to close this window...")
        raise e

if __name__ == "__main__":
    from PyQt6.QtCore import QThread
    main()
