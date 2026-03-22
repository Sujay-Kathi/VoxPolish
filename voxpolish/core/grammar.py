import os
import requests
import json
from dotenv import load_dotenv

class NvidiaPolisher:
    """
    Grammar and Punctuation Polisher using NVIDIA NIM (Llama 3.1 70B).
    Strictly preserves the original word-for-word spoken sequence.
    """
    def __init__(self, api_key=None):
        if api_key is None:
            # Load from .env if not provided directly
            import sys
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
            env_path = os.path.join(base_path, ".env")
            
            if not os.path.exists(env_path):
                alt_env = os.path.join(base_path, "_internal", ".env")
                if os.path.exists(alt_env):
                    env_path = alt_env
            
            load_dotenv(env_path)
            api_key = os.getenv("NVIDIA_API_KEY")
            
        if not api_key:
            print("Warning: NVIDIA_API_KEY not found. Grammar polishing will be skipped.", flush=True)
            self.api_key = None
            return

        self.api_key = api_key
        self.api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.model_id = "meta/llama-3.1-70b-instruct"
        
        # PROSE MODE: Strict verbatim punctuation
        self.prose_instruction = (
            "You are a verbatim text formatter. Restore punctuation and capitalization to the text. "
            "CRITICAL: DO NOT change, add, or remove any words. KEEP the exact word-for-word spoken sequence. "
            "Output ONLY the corrected text. Do not explain."
        )

        # TECHNICAL MODE: Preserve code-style case sensitivity and formatting
        self.technical_instruction = (
            "Restore technical punctuation and capitalization for a developer context. "
            "DO NOT rephrase. Keep technical terms exactly as spoken but formatted correctly (e.g., 'setup py' becomes 'setup.py'). "
            "DO NOT change word order. Output ONLY the formatted text."
        )

    def polish(self, text, mode='prose'):
        """
        Sends raw text to NVIDIA NIM and returns the polished version.
        mode: 'prose' or 'technical' (mapped to 'standard'/'coding' from main)
        """
        if not self.api_key or not text.strip():
            return text

        # Map UI modes to instructions
        instruction = self.technical_instruction if mode in ['technical', 'coding'] else self.prose_instruction

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model_id,
                "messages": [
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.1, # Low temperature for max predictability
                "top_p": 0.7,
                "max_tokens": 1024
            }

            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            polished_text = data['choices'][0]['message']['content'].strip()
            
            # Final sanity check: if the model drastically changed length, fallback to raw
            if len(polished_text.split()) > len(text.split()) + 5 or len(polished_text.split()) < len(text.split()) - 5:
                print("Warning: Model rephrased too aggressively. Using raw text.")
                return text
                
            return polished_text
            
        except Exception as e:
            print(f"NVIDIA API Error ({mode}): {e}", flush=True)
            return text

if __name__ == "__main__":
    polisher = NvidiaPolisher()
    test_text = "i am going toi get the nividia nim apis for the model"
    print(f"Polishing Test: {polisher.polish(test_text)}")
