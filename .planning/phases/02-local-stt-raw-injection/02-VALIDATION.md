# Phase 2: Local STT & Raw Injection - Validation Strategy

**Phase:** 02
**Slug:** local-stt-raw-injection
**Defined:** 2026-03-22

## Validation Objective
To verify that the "Speech-to-Text" (AUST-02) and "Injection" (INJS-01) loops are robust and accurately synchronized with the system-wide hotkeys.

## Dimension 8: Validation Architecture

### STT & STUB check
- [ ] **ST-01: Whisper Integration** — The `voxpolish.core.stt` module can successfully initialize and transcribe a pre-recorded `.wav` file (or synthetic byte stream).
- [ ] **ST-02: Latency** — Transcription of a 2-second snippet takes <500ms on a single CPU core.

### Hotkey & Interaction
- [ ] **HK-01: Global Hotkey Listener** — Pressing `Ctrl + Alt + Z` successfully toggles the `AudioCollector` state.
- [ ] **HK-02: User Interruption** — Hotkey works even if the user is typing in another application.

### Injection
- [ ] **IJ-01: Buffer Typing** — Transcribed text is successfully "typed" with `keyboard.write()` into a blank Notepad window.
- [ ] **IJ-02: No Auto-Enter** — Verify that NO "Enter" or submit signal follows the text injection.

## Verification Methods

### Automated Tests
- `pytest tests/test_stt.py` — Verifying the STT results on test audio.
- `scripts/verify_hotkey.py` — Tool to print a message to the console every time the hotkey is triggered.

### Manual Verification
- Run the app, open Notepad, press `Ctrl + Alt + Z`, speak "Hello, this is a test," press hotkey again. Result: "Hello, this is a test" appears in Notepad.

---
*Validation strategy for Phase 2.*
