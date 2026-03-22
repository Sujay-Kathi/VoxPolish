import numpy as np
import time
import os
import sys
import io
import wave
import traceback
import grpc
import riva.client
from dotenv import load_dotenv

class NvidiaSTT:
    """
    STT Engine using NVIDIA NIM/Riva (Hosted gRPC).
    Optimized for the latest Riva Python client and hosted NVCF endpoints.
    """
    def __init__(self, model_size="default", device="auto", compute_type="default"):
        self.api_key = None
        # Load .env
        import sys
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        env_path = os.path.join(base_path, ".env")
        if not os.path.exists(env_path):
            alt_env = os.path.join(base_path, "_internal", ".env")
            if os.path.exists(alt_env):
                env_path = alt_env
        
        load_dotenv(env_path)
        self.api_key = os.getenv("NVIDIA_API_KEY")
        
        # Hosted NVCF URI for Riva/ASR
        self.uri = "grpc.nvcf.nvidia.com:443"
        # Parakeet CTC 1.1b Function ID
        self.function_id = "1598d209-5e27-4d3c-8079-4751568b1081"
        
        print("Initializing NVIDIA gRPC STT Engine...", flush=True)

    def transcribe(self, audio_data):
        if audio_data is None or len(audio_data) == 0:
            return ""

        if not self.api_key:
            print("ERROR: NVIDIA_API_KEY not found in .env.", flush=True)
            return "STT Client Missing"

        return self._transcribe_grpc(audio_data)

    def _transcribe_grpc(self, audio_data):
        """Sends audio to NVIDIA NIM via gRPC (Hosted NVCF)."""
        try:
            print("Transcription: Processing via NVIDIA gRPC...", flush=True)
            
            # 1. Setup Auth with NVCF Metadata
            auth = riva.client.Auth(
                uri=self.uri,
                use_ssl=True,
                metadata_args=[
                    ("authorization", f"Bearer {self.api_key}"),
                    ("function-id", self.function_id)
                ]
            )
            
            # 2. Create Riva ASR Client
            client = riva.client.ASRService(auth)
            
            # 3. Configure Request (Removed enable_manual_punctuation to fix API mismatch)
            config = riva.client.RecognitionConfig(
                encoding=riva.client.AudioEncoding.LINEAR_PCM,
                sample_rate_hertz=16000,
                language_code="en-US",
                max_alternatives=1,
                enable_automatic_punctuation=True,
                audio_channel_count=1
            )
            
            # 4. Perform Sync Offline Transcription
            audio_bytes = audio_data.tobytes()
            
            response = client.offline_recognize(audio_bytes, config)
            
            if response.results:
                text = response.results[0].alternatives[0].transcript.strip()
                print(f"NVIDIA gRPC Completion: {text[:50]}...", flush=True)
                return text
            
            return ""
            
        except Exception as e:
            # Catching the field error or connection issues
            print(f"NVIDIA gRPC Error: {e}", flush=True)
            return ""

if __name__ == "__main__":
    print("NVIDIA gRPC STT Engine loaded.")
