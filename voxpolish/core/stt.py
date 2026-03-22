import os
import numpy as np
from faster_whisper import WhisperModel
import time

class WhisperSTT:
    """
    STT Engine using faster-whisper (ctranslate2).
    Optimized for low-latency CPU transcription.
    """
    def __init__(self, model_size="tiny.en", device="cpu", compute_type="int8"):
        print(f"Initializing STT Engine ({model_size})...", flush=True)
        start_time = time.time()
        # model is downloaded on first init
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print(f"STT Engine ready in {time.time() - start_time:.2f}s", flush=True)

    def transcribe(self, audio_data):
        """
        Transcribes numpy int16 audio data.
        Returns the concatenated text string.
        """
        if audio_data is None or len(audio_data) == 0:
            return ""

        # Convert int16 to float32 between -1 and 1
        audio_float = audio_data.astype(np.float32) / 32768.0
        
        # Transcribe
        # beam_size=1 for speed, vad_filter=True for silence trimming
        segments, info = self.model.transcribe(audio_float, beam_size=1, vad_filter=True)
        
        text_segments = [segment.text for segment in segments]
        full_text = "".join(text_segments).strip()
        
        return full_text

if __name__ == "__main__":
    # Quick test stub if run directly
    stt = WhisperSTT()
    # Generate 1s of silence
    silence = np.zeros(16000, dtype=np.int16)
    print("Test transcription (silence):", stt.transcribe(silence))
