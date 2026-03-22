import json
import os
from datetime import datetime

class AppDataManager:
    def __init__(self, filepath="voxpolish_data.json"):
        self.filepath = filepath
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "history": [],
            "settings": {
                "hotkey": "ctrl+alt+z",
                "coding_hotkey": "ctrl+alt+c"
            }
        }

    def _save(self):
        try:
            with open(self.filepath, "w") as f:
                json.dump(self.data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def add_history(self, text, mode):
        # Insert at top, keep last 50
        self.data["history"].insert(0, {
            "text": text,
            "mode": mode,
            "timestamp": datetime.now().isoformat()
        })
        self.data["history"] = self.data["history"][:50]
        self._save()

    def get_history(self):
        return self.data.get("history", [])

data_manager = AppDataManager()
