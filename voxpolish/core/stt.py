import numpy as np
import time
import os
import sys
import io
import wave
import traceback
import requests
import json
from dotenv import load_dotenv

class NvidiaSTT:
    """
    STT Engine using NVIDIA NIM ASR (Parakeet).
    Replaces Gemini for verbatim transcription.
    """
    def __init__(self, model_size="default", device="auto", compute_type="default"):
        self.api_key = None
        # Use the same .env logic as grammar.py
        import sys
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        env_path = os.path.join(base_path, ".env")
        if not os.path.exists(env_path):
            alt_env = os.path.join(base_path, "_internal", ".env")
            if os.path.exists(alt_env):
                env_path = alt_env
        
        load_dotenv(env_path)
        self.api_key = os.getenv("NVIDIA_API_KEY")
        
        # Hosted NVIDIA ASR Endpoint (Build.nvidia.com style)
        self.api_url = "https://integrate.api.nvidia.com/v1/audio/transcriptions"
        self.model_id = "nvidia/parakeet-ctc-1.1b" # Standard Parakeet choice
        
        print("Initializing NVIDIA NIM STT Engine...", flush=True)

    def transcribe(self, audio_data):
        if audio_data is None or len(audio_data) == 0:
            return ""

        if not self.api_key:
            print("ERROR: NVIDIA_API_KEY not found in .env. STT failed.", flush=True)
            return "STT Client Missing"

        return self._transcribe_nvidia(audio_data)

    def _transcribe_nvidia(self, audio_data):
        """Sends audio to NVIDIA NIM for transcription via REST."""
        try:
            print("Transcription: Processing via NVIDIA NIM...", flush=True)
            
            # Convert numpy to WAV bytes (16kHz Mono)
            buffer = io.BytesIO()
            with wave.open(buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio_data.tobytes())
            
            audio_bytes = buffer.getvalue()
            
            # Prepare Multipart Request (OpenAI/NIM Standard)
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            files = {
                'file': ('audio.wav', audio_bytes, 'audio/wav')
            }
            
            data = {
                'model': self.model_id,
                'response_format': 'json'
            }
            
            # Note: Timeout is slightly longer for audio processing
            response = requests.post(self.api_url, headers=headers, files=files, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            text = result.get("text", "").strip()
            
            print(f"NVIDIA Transcription Complete: {text[:50]}...", flush=True)
            return text
            
        except Exception as e:
            print(f"NVIDIA STT Error: {e}", flush=True)
            # Fallback to a clear message
            return f""

if __name__ == "__main__":
    print("NVIDIA STT Engine loaded.")
