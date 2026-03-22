# Phase 1: Project Setup & Base Audio - Research

**Phase:** 01
**Researched:** 2026-03-22
**Confidence:** HIGH

## Implementation Patterns

### 1. Sounddevice + WebRTCVAD Integration
To achieve low-latency silence detection, `sounddevice` must feed `webrtcvad` with precise frame sizes (10ms, 20ms, or 30ms).

- **Sample Rate:** 16,000 Hz (standard for Faster-Whisper and supported by webrtcvad).
- **Frame Size:** 30ms (480 samples @ 16kHz).
- **Callback Pattern:** Use `sd.InputStream` with a callback to push frames into a thread-safe `queue.Queue`.

```python
import sounddevice as sd
import webrtcvad

vad = webrtcvad.Vad(3) # Aggressiveness 0-3
# webrtcvad frame must be 10, 20, or 30ms
# samplerate=16000, 30ms -> 480 samples
```

### 2. Producer-Consumer Threading
- **Producer Thread:** Captures raw audio via `sounddevice` callback and puts chunks into a queue.
- **Consumer Thread:** Pulls from the queue, runs `webrtcvad.is_speech()`, and buffers data if speech is detected.
- **Mechanism:** Use a flag or `Event` to signal the start/stop of the recording process.

### 3. Modular Project Layout
```
voxpolish/
├── core/
│   ├── __init__.py
│   ├── audio.py      # sounddevice + webrtcvad logic
│   ├── stt.py        # Faster-Whisper wrapper (stub for now)
│   └── grammar.py    # Gemini API client (stub for now)
├── requirements.txt
└── main.py           # Entry point
```

## Validation Architecture

To ensure the "Base Audio" is robust (AUST-01), we must validate:
1. **Audio Levels:** Verify the system can hear the user (RMS calculation).
2. **VAD Accuracy:** Verify the silence detection correctly identifies pauses vs speech.
3. **Queue Health:** Ensure the buffer doesn't overflow or drop frames.

## Technical Pitfalls
- **Admin Perms:** Windows may block microphone access; must handle `PortAudioError` gracefully.
- **Blocking Callbacks:** The audio callback must be fast; do NOT perform VAD inside the callback.

---
*Research for Phase 1 complete.*
