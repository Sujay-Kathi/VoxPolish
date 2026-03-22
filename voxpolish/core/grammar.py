import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

class GeminiPolisher:
    """
    Grammar and Punctuation Polisher using Google Gemini 2.5-Flash.
    Supports Dual Modes: Prose (Friendly) and Technical (Coding).
    """
    def __init__(self, api_key=None):
        if api_key is None:
            import sys
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
            env_path = os.path.join(base_path, ".env")
            
            # Use _internal if needed
            if not os.path.exists(env_path):
                alt_env = os.path.join(base_path, "_internal", ".env")
                if os.path.exists(alt_env):
                    env_path = alt_env
            
            load_dotenv(env_path)
            api_key = os.getenv("GEMINI_API_KEY")
            
        if not api_key:
            print("Warning: GEMINI_API_KEY not found. Grammar polishing skipped.", flush=True)
            self.client = None
            self.prose_instruction = None
            self.technical_instruction = None
            return

        self.client = genai.Client(api_key=api_key)
        self.model_id = "gemini-2.5-flash"
        
        # Prose Mode: Only add punctuation, NO CHANGING WORDS
        self.prose_instruction = (
            "Restore punctuation and capitalization to the following text. "
            "DO NOT CHANGE, ADD, OR REMOVE ANY WORDS. "
            "Keep the phrasing EXACTLY as provided. Verbatim text only."
        )

        # Technical Mode: Preserve case-sensitivity, no extra prose
        self.technical_instruction = (
            "Restore technical punctuation and capitalization. "
            "DO NOT REPHRASE. DO NOT ADD INTRODUCTIONS. "
            "Maintain exact word order and formatting. "
        )

    def polish(self, text, mode='prose'):
        """
        Sends raw text to Gemini and returns the polished version based on the mode.
        mode: 'prose' or 'technical'
        """
        if not self.client or not text.strip():
            return text

        instruction = self.technical_instruction if mode == 'technical' else self.prose_instruction

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=text,
                config=types.GenerateContentConfig(
                    system_instruction=instruction
                )
            )
            polished_text = response.text.strip()
            return polished_text if polished_text else text
        except Exception as e:
            print(f"Gemini API Error ({mode}): {e}", flush=True)
            return text

if __name__ == "__main__":
    polisher = GeminiPolisher()
    test_code = "find all items in the list and then filter by category"
    print(f"Technical: {polisher.polish(test_code, mode='technical')}")
