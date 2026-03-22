import os
import sys
import numpy as np

class WakeWordListener:
    """
    Wake word detection using openwakeword.
    Handles binary loading failures gracefully.
    """
    def __init__(self, model_names=None, threshold=0.5):
        self.model_names = model_names or ["alexa", "hey_mycroft"]
        self.threshold = threshold
        self.oww_model = None
        self.is_active = False
        
        print(f"Initializing Wake Word Engine...", flush=True)
        try:
            # 1. DEFERRED IMPORT: This is critical. Don't let the import crash the app.
            import openwakeword
            from openwakeword.model import Model
            
            # Setup path finding (PyInstaller support)
            base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
            
            # Look for models in the _internal folder if frozen
            model_paths = []
            for name in self.model_names:
                # 1. Check Root
                p1 = os.path.join(base_path, "voxpolish", "assets", "models", "wakeword", f"{name}_v0.1.onnx")
                # 2. Check _internal
                p2 = os.path.join(base_path, "_internal", "openwakeword", "resources", "models", f"{name}_v0.1.onnx")
                
                # Helper to check if file is a valid model (not a 9-byte placeholder)
                def is_valid(path):
                    return os.path.exists(path) and os.path.getsize(path) > 1024
                
                if is_valid(p1):
                    model_paths.append(p1)
                elif is_valid(p2):
                    model_paths.append(p2)
                else:
                    # Fallback to the package's internal path
                    m_path = os.path.join(os.path.dirname(openwakeword.__file__), "resources", "models", f"{name}_v0.1.onnx")
                    if is_valid(m_path):
                        model_paths.append(m_path)

            if model_paths:
                print(f"Loading {len(model_paths)} Wake Models: {model_paths}", flush=True)
                # This call can crash if ONNXRuntime is broken
                self.oww_model = Model(wakeword_models=model_paths)
                self.is_active = True
                print(f"Wake Word detection active (Threshold: {self.threshold}).", flush=True)
            else:
                print("Wake models not found in any search path.", flush=True)
                
        except Exception as e:
            print(f"Wake Word Engine failed (Binary Load Error): {e}. Voice activation skipped.", flush=True)
            self.oww_model = None
            self.is_active = False

    def predict(self, chunk):
        """
        Receives 16kHz audio chunk and returns True if wake word is detected.
        Safe to call even if model failed to load.
        """
        if not self.is_active or not self.oww_model:
            return False
            
        try:
            # Expects numpy int16
            prediction = self.oww_model.predict(chunk)
            # Returns a dict of model_name: score
            for name, score in prediction.items():
                if score > self.threshold:
                    print(f"WAKE WORD DETECTED: {name} (Score: {score:.2f})", flush=True)
                    return True
        except Exception:
            # Silent fail on predict error
            pass
            
        return False
