# Architecture Research

**Domain:** Desktop Speech-to-Text Utility
**Researched:** 2026-03-22
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ System  │  │ Status  │  │ Settings│  │ Hotkey  │        │
│  │ Tray    │  │ Overlay │  │ Manager │  │ Listener│        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
│       │            │            │            │              │
├───────┴────────────┴────────────┴────────────┴──────────────┤
│                        Business Logic                       │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────────────────┐    ┌─────────────────────┐    │
│  │ Wake Word Engine (ONNX)│    │ Audio Buffer (Queue)│    │
│  └────────────────────────┘    └─────────────────────┘    │
│  ┌────────────────────────┐    ┌─────────────────────┐    │
│  │   STT Processor        │    │ Grammar Polisher    │    │
│  │ (Faster-Whisper)       │    │ (Gemini API)        │    │
│  └────────────────────────┘    └─────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                        System Gateway                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │  Hotkey  │  │  Keyboard│  │ Microphone│                   │
│  │  Manager │  │  Injector│  │ Wrapper   │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Wake Word Engine | Background listening for "Vox". | `openWakeWord` with lightweight ONNX model on CPU. |
| STT Processor | Audio chunk -> Raw text transcription. | `Faster-Whisper` (tiny.en for speed). |
| Grammar Polisher | Raw text -> Polished, punctuated prose. | `google-generativeai` (Gemini 3 Flash). |
| Keyboard Injector | Simulating keystrokes into active app. | `keyboard` or `pynput` library. |
| Tray Manager | Visual feedback and mode switching. | `PyQt6` system tray integration. |

## Recommended Project Structure

```
src/
├── app/                # Main application loop and UI
│   ├── tray.py         # System tray and menu
│   ├── overlay.py      # "Listening" indicator on screen
│   └── settings.py     # Persistent config management
├── core/               # Business logic
│   ├── stt.py          # Faster-Whisper wrapper
│   ├── grammar.py      # Gemini API client
│   └── wakeword.py     # openWakeWord listener
├── utils/              # System interfaces
│   ├── audio.py        # Sounddevice / PyAudio wrappers
│   └── keyboard.py     # Keyboard injection/hotkeys
└── main.py             # App entry point
```

### Structure Rationale

- **app/:** Isolates the UI logic from core ML tasks, maintaining separation of concerns between state and interface.
- **core/:** Distinct modules for STT/Grammar/WakeWord for easy model swapping later.
- **utils/:** General-purpose low-level system wrappers.

## Architectural Patterns

### Pattern 1: Producer-Consumer Audio Pipeline

**What:** Multi-threaded audio handling where one thread records to a queue and another processes transcription.
**When to use:** Continuous listening settings where recording must never drop chunks.
**Trade-offs:** Increases complexity (thread safety) but ensures no speech is lost during heavy LLM inference.

### Pattern 2: State-Controlled Overlay

**What:** A non-interrupting floating window (semi-transparent) that reflects the app's current state (IDLE, LISTENING, POLISHING).
**When to use:** In IDEs where the user needs visual confirmation they are being "heard."
**Trade-offs:** Adds UI complexity; must stay "topmost" without stealing focus.

## Data Flow

### Transcription Flow

```
[Audio Input]
    ↓
[VAD / Whisper Engine] → [Raw Transcription Buffer]
    ↓
[Gemini Polisher] → [Polished Text Block]
    ↓
[Keyboard Injector] ──injects──> [Target IDE/Editor]
```

### State Management

```
[App State (Enum)]
    ↓ (signal)
[System Tray Icon] ←→ [Event Handlers] → [State Update] → [Tray Icon / Overlay]
```

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| Single User | Desktop app with local STT is efficient and private. |
| Multi-User | Needs centralized API key management or cloud-based STT. |

### Scaling Priorities

1. **CPU Usage:** Transcription is CPU-heavy. Scaling involves model quantization (`int8`) or using external APIs.
2. **Memory:** Large Whisper models burn RAM; tiny/base models needed for "any spec" consistency.

## Anti-Patterns

### Anti-Pattern 1: Large Local LLMs for Low-Spec

**What people do:** Attempt to run Llama-3-8B locally for grammar.
**Why it's wrong:** Smashes RAM and slows transcription to minutes.
**Do this instead:** Use hyper-optimized cloud free tiers (Gemini Flash) for the grammar layer.

### Anti-Pattern 2: Direct "Key-by-Key" Typing of Large Blocks

**What people do:** Simulating individual `keydown/up` events for long sentences.
**Why it's wrong:** Can lag or produce race conditions with user's auto-suggestions in IDEs.
**Do this instead:** Inject large text blocks via the clipboard or "type string" higher-level abstractions.

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Google AI Studio | Official SDK (REST) | Free-tier token limits (RPM) must be handled gracefully in UI. |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Audio -> Core | Thread-safe queue | Ensures zero audio loss during processing lag. |

## Sources

- PyOS and Keyboard Integration Best Practices.
- Google Gemini FLASH architecture whitepaper.
- Faster-Whisper implementation patterns on GitHub.

---
*Architecture research for: Desktop Speech-to-Text Utility*
*Researched: 2026-03-22*
