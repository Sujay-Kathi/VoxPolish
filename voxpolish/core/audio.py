import queue
import threading
import numpy as np
import sounddevice as sd
import webrtcvad
import time

class AudioCollector:
    """
    Producer-Consumer audio capture using sounddevice and webrtcvad.
    Captures raw 16-bit PCM audio @ 16kHz in 30ms frames.
    """
    def __init__(self, sample_rate=16000, frame_duration_ms=30, vad_aggressiveness=3):
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        self.vad = webrtcvad.Vad(vad_aggressiveness)
        
        self.audio_queue = queue.Queue()
        self.is_recording = threading.Event()
        self.speech_buffer = []
        
        self.stream = None
        self.consumer_thread = None

    def _audio_callback(self, indata, frames, time_info, status):
        """Producer: callback for sounddevice InputStream."""
        if status:
            print(f"Status bit: {status}", flush=True)
        # Push raw int16 data into the queue
        self.audio_queue.put(indata.copy())

    def _consume_audio(self):
        """Consumer: Extract frames from queue and run VAD."""
        print("Audio consumer thread started.", flush=True)
        while self.is_recording.is_set() or not self.audio_queue.empty():
            try:
                # get chunk (blocksize=480 for 30ms @ 16k)
                chunk = self.audio_queue.get(timeout=0.1)
                
                # Convert to bytes for webrtcvad
                raw_bytes = chunk.tobytes()
                
                # VAD check
                is_speech = self.vad.is_speech(raw_bytes, self.sample_rate)
                
                if is_speech:
                    self.speech_buffer.append(chunk)
                
                # Logic for triggering STT would go here in later phases
                
            except queue.Empty:
                continue
        print("Audio consumer thread stopped.", flush=True)

    def start(self):
        """Start the audio stream and consumer thread."""
        if self.is_recording.is_set():
            return
            
        self.is_recording.set()
        self.speech_buffer = []
        
        # Start consumer
        self.consumer_thread = threading.Thread(target=self._consume_audio)
        self.consumer_thread.start()
        
        # Start recording with sounddevice
        # blocksize=480 ensures 30ms chunks at 16000Hz
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16',
            blocksize=self.frame_size,
            callback=self._audio_callback
        )
        self.stream.start()
        print(f"Recording started... (SR={self.sample_rate}, Block={self.frame_size})", flush=True)

    def stop(self):
        """Stop recording and processing."""
        if not self.is_recording.is_set():
            return
            
        self.is_recording.clear()
        if self.stream:
            self.stream.stop()
            self.stream.close()
        
        if self.consumer_thread:
            self.consumer_thread.join()
        
        print("Recording stopped.", flush=True)

    def get_captured_audio(self):
        """Returns the concatenated speech buffer as a single numpy array."""
        if not self.speech_buffer:
            return np.array([], dtype='int16')
        return np.concatenate(self.speech_buffer)

if __name__ == "__main__":
    # Test stub
    collector = AudioCollector()
    collector.start()
    time.sleep(3)
    collector.stop()
    print(f"Captured {len(collector.get_captured_audio())} samples.")
