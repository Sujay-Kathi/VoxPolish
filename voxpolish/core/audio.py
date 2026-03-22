import sounddevice as sd
import numpy as np
import queue
import threading
import webrtcvad

class AudioCollector:
    """
    Continuous microphone stream manager.
    Refactored to be 'always-on' to support both wake-word 
    detection and speech-to-STT capture without MIC re-initialization.
    """
    def __init__(self, sample_rate=16000, frame_duration_ms=30):
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)
        
        # WebRTCVAD initialization (Mode 3 is most aggressive)
        self.vad = webrtcvad.Vad(3)
        
        # Buffers & Queues
        self.audio_queue = queue.Queue() # Raw stream -> Consumer (STT)
        self.wake_queue = queue.Queue()  # Raw stream -> Wake Word engine
        self.speech_buffer = [] # Speech frames only (for STT)
        self.latest_chunk = None # Single latest chunk (legacy support)
        
        # Flags
        self.is_running = threading.Event()
        self.is_capturing_speech = threading.Event() # Controls if data goes to speech_buffer
        
        # Multi-threading
        self.stream = None
        self._consumer_thread = None

    def _audio_callback(self, indata, frames, time, status):
        """Simple callback: pushes raw int16 data into the queues."""
        if status:
            print(f"SD Status: {status}", flush=True)
        # Put a flat copy of the chunk into the queues
        chunk = indata.flatten().copy()
        self.audio_queue.put(chunk)
        self.wake_queue.put(chunk)
        self.latest_chunk = chunk

    def start_stream(self):
        """Opens the hardware microphone stream 'always-on'."""
        if self.stream is not None:
            return
            
        self.is_running.set()
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16',
            blocksize=self.frame_size,
            callback=self._audio_callback
        )
        self.stream.start()
        
        # Start the background consumer thread
        self._consumer_thread = threading.Thread(target=self._consume_audio, daemon=True)
        self._consumer_thread.start()
        print("Microphone hardware and consumer thread started.", flush=True)

    def _consume_audio(self):
        """Background thread that drains the audio_queue and fills the speech buffer."""
        while self.is_running.is_set():
            try:
                # Use a small timeout to keep checking is_running
                chunk = self.audio_queue.get(timeout=0.1)
                if self.is_capturing_speech.is_set():
                    self.speech_buffer.append(chunk)
            except queue.Empty:
                continue

    def stop_hardware(self):
        """Completely shuts down the hardware stream."""
        self.is_running.clear()
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        print("Microphone hardware stopped.", flush=True)

    def start(self):
        """Start capturing speech (called by the UI worker)."""
        self.speech_buffer = []
        # Clear wake queue to avoid triggering on old audio when listening starts? 
        # No, wake word only runs when not recording.
        self.is_capturing_speech.set()

    def stop(self):
        """Stop capturing speech and return the buffer."""
        self.is_capturing_speech.clear()
        return self.get_captured_audio()

    def get_captured_audio(self):
        """Returns concatenated speech buffer as int16."""
        if not self.speech_buffer:
            return np.array([], dtype='int16')
        return np.concatenate(self.speech_buffer)

    def get_next_wake_chunk(self):
        """Returns the next chunk from the wake queue (blocking)."""
        try:
            return self.wake_queue.get(timeout=0.2)
        except queue.Empty:
            return None

    def get_latest_chunk(self):
        """Returns the latest captured chunk (legacy support)."""
        return self.latest_chunk

    def is_speech(self, chunk):
        """VAD check: is this chunk speech? (requires 16-bit PCM)."""
        if chunk is None or len(chunk) != self.frame_size:
            return False
        return self.vad.is_speech(chunk.tobytes(), self.sample_rate)
