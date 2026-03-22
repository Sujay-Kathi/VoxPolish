# Phase 2: Local STT & Raw Injection - Research

**Phase:** 02
**Researched:** 2026-03-22
**Confidence:** HIGH

## Implementation Patterns

### 1. Faster-Whisper (ctranslate2) Integration
To achieve <500ms latency on low-spec hardware (CPU):
- **Model:** `"tiny.en"` (specifically for English, smaller/faster than `"tiny"`).
- **Device:** `"cpu"`.
- **Compute Type:** `"int8"` (quantized model for speed).

```python
from faster_whisper import WhisperModel
model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
segments, info = model.transcribe(audio_np, beam_size=1)
```

### 2. Global Hotkeys and Keyboard Injection
- **Library:** `keyboard` (highly effective on Windows).
- **Toggle Mechanism:** Track a `is_recording` state and trigger `start()` / `stop()` on `AudioCollector`.

```python
import keyboard
keyboard.add_hotkey('ctrl+alt+z', self._toggle_recording)
keyboard.write(transcription) # system-wide injection
```

### 3. Silence Trimming
- **Trimming Logic:** `faster-whisper` returns `segments`. We'll use the `start` and `end` times of the first/last valid speech segments to crop the raw buffer, reducing useless processing in the grammar phase (Phase 3).

## Validation Architecture

To ensure the "STT & Injection" loop (AUST-02, INJS-01) is robust, we must validate:
1. **Hotkey Integrity:** Hotkey triggers even when a focus-stealing app (like Notepad) is active.
2. **Transcription Speed:** Full pipeline (Audio -> STT -> Injection) under 1 second.
3. **Typing Accuracy:** Ensure special characters (if any) are correctly injected.

## Technical Pitfalls
- **Cold Boot:** The first transcription can be slow due to model loading. **Solution:** Pre-load the model in `voxpolish/core/stt.py` during app init.
- **Race conditions:** User might start speaking before the hotkey registers or after they think it stopped. **Solution:** Visual feedback (Phase 6) and immediate state toggle.

---
*Research for Phase 2 complete.*
