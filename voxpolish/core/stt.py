import numpy as np
import time
import os
import sys
import io
import wave
import traceback

class WhisperSTT:
    """
    ULTRA-STABLE STT Engine using Google Gemini (Cloud).
    Removed all local faster-whisper/ctranslate2 dependencies to fix binary crashes on Windows.
    """
    def __init__(self, model_size="tiny.en", device="auto", compute_type="default"):
        self.cloud_client = None
        print("Initializing High-Stability Cloud STT Engine...", flush=True)

    def set_cloud_client(self, client):
        """Hook into the Gemini client."""
        self.cloud_client = client

    def transcribe(self, audio_data):
        if audio_data is None or len(audio_data) == 0:
            return ""

        if not self.cloud_client:
            print("ERROR: Cloud STT client not initialized. Check GEMINI_API_KEY.", flush=True)
            return "STT Client Missing"

        return self._transcribe_cloud(audio_data)

    def _transcribe_cloud(self, audio_data):
        """Sends audio to Gemini for transcription."""
        try:
            from google.genai import types
            print("Transcription: Processing via Gemini Cloud...", flush=True)
            
            # Convert numpy to WAV bytes (16kHz Mono)
            buffer = io.BytesIO()
            with wave.open(buffer, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio_data.tobytes())
            
            audio_bytes = buffer.getvalue()
            
            # Use Gemini to transcribe verbatim
            response = self.cloud_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[
                    "Transcribe the audio VERBATIM. DO NOT CHANGE ANY WORDS. "
                    "Only output the exact spoken text. No comments, no formatting.",
                    types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav")
                ]
            )
            
            text = response.text.strip()
            # Clean text from common Gemini prefixes or markdown
            if text.startswith("Transcription:"):
                 text = text.replace("Transcription:", "").strip()
            
            print(f"Transcription Complete: {text[:50]}...", flush=True)
            return text
        except Exception as e:
            print(f"Cloud STT Error: {e}", flush=True)
            return f"Transcribe Error: {e}"

if __name__ == "__main__":
    print("Cloud STT Engine loaded.")
