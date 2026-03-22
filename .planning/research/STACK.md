# Stack Research

**Domain:** Desktop Speech-to-Text Utility
**Researched:** 2026-03-22
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.11+ | Logic & ML Glue | Best ecosystem for local ML models (Whisper, ONNX) and cross-platform OS hooks. |
| Faster-Whisper | 0.10+ | STT Engine | CTranslate2 re-implementation of Whisper. 4x faster and uses significantly less memory than OpenAI's original. |
| Gemini 3 Flash | v1 (Free) | Grammar/Code AI | Best-in-class performance for sub-second text polishing. Generous free tier (15 RPM) perfect for personal use. |
| keyboard | latest | Input Injection | Simple, cross-platform global hotkeys and system-wide keyboard simulation. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| openWakeWord | 0.5+ | Wake Word Detection | Low-resource ONNX-based wake word engine. Robust for "Vox" triggering. |
| PyQt6 | 6.5+ | Desktop GUI | Modern, fast, and light compared to Electron. Critical for the "any spec" requirement. |
| google-generativeai | latest | AI Studio SDK | Official Google SDK for interacting with the Gemini API. |
| sounddevice | latest | Audio Capture | Efficient portaudio-based audio recording with low latency. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| PyInstaller | Binary Bundling | Used to create a standalone `.exe` for Windows so the user doesn't need to install Python. |
| ONNX Runtime | ML Inference | Required for `openWakeWord` and `Faster-Whisper` CPU execution. |

## Installation

```bash
# Core
pip install faster-whisper google-generativeai keyboard PyQt6

# Supporting
pip install openWakeWord sounddevice numpy
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Faster-Whisper | whisper.cpp | If building a C++ native app; however, Python bindings for Faster-Whisper are more mature for quick dev. |
| Gemini 3 Flash | Groq (Llama 3) | If ultra-low latency is required (<100ms), though Gemini handles technical/coding context better in 2025. |
| PyQt6 | Electron | If building a highly complex, web-heavy UI; avoid for this project due to RAM constraints on "any spec" PCs. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| OpenAI Whisper (Original) | Too heavy for low-spec CPU usage. | Faster-Whisper |
| Windows built-in STT | Requires internet and lacks technical accuracy for coding/prompting. | Local Faster-Whisper |
| Selenium/WebDriver | Overkill for text injection. | `keyboard` library |

## Stack Patterns by Variant

**If Low Memory (<4GB RAM):**
- Use `whisper-tiny` model (75MB RAM).
- Disable wake word; use hotkey only to conserve CPU.

**If Reliable Internet:**
- Use Gemini Flash 3 API for grammar (saves local CPU).

**If Offline Focus:**
- Swap Gemini for a local GGUF model via LLAMA.cpp (requires higher specs).

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| Faster-Whisper | ONNX Runtime 1.16+ | Critical for CPU optimization. |
| keyboard | Windows Admin | Requires admin privileges for global input injection in some apps. |

## Sources

- [Faster-Whisper GitHub] — Verified performance benchmarks vs original Whisper.
- [Google AI Studio Docs] — Verified Gemini Flash free tier limits and technical capabilities.
- [openWakeWord Docs] — Verified Raspberry Pi (low resource) compatibility.

---
*Stack research for: Desktop Speech-to-Text Utility*
*Researched: 2026-03-22*
