# Roadmap: VoxPolish

## Overview

VoxPolish will be built in six strategic phases, moving from the foundational "Record and Type" loop to a sophisticated, AI-driven voice polisher that understands technical context and operates entirely hands-free.

## Phases

- [ ] **Phase 1: Project Setup & Base Audio** - Initialize the Python environment and build the low-latency audio capture pipeline.
- [ ] **Phase 2: Local STT & Raw Injection** - Implement Faster-Whisper and the global hotkey system for immediate "speech-to-text" functionality.
- [ ] **Phase 3: AI Polisher (Grammar API)** - Integrate the Gemini 3 Flash API to transform raw transcripts into punctuated, professional prose.
- [ ] **Phase 4: Technical Presets (Coding Mode)** - Refine the AI layer to preserve code syntax, case sensitivity, and technical keywords for IDE use.
- [ ] **Phase 5: Wake Word ("Vox") Triggering** - Add the hands-free "Vox" wake word listener for frictionless activation.
- [ ] **Phase 6: Visual Feedback & UI** - Build the system tray menu and a persistent status overlay to provide user feedback.

## Phase Details

### Phase 1: Project Setup & Base Audio
**Goal**: Establish the development environment and a robust Producer-Consumer audio recording thread.
**Depends on**: Nothing
**Requirements**: AUST-01
**Success Criteria**:
  1. Python 3.11 environment is configured with all research stack dependencies.
  2. System can successfully capture audio from the default microphone without dropping samples.
  3. Audio data is piped into a thread-safe queue ready for processing.
**Plans**: 2 plans

Plans:
- [x] 01-01: Environment initialization and dependency scaffolding.
- [x] 01-02: Multi-threaded audio capture implementation.

### Phase 2: Local STT & Raw Injection
**Goal**: Build the core "Speech-to-Text" functionality using local models and global OS hotkeys.
**Depends on**: Phase 1
**Requirements**: AUST-02, AUST-03, INJS-01, INJS-02
**Success Criteria**:
  1. `Faster-Whisper` (tiny.en) transcribes audio with <500ms latency.
  2. Global hotkey (Win+Shift+V) successfully toggles the recording state.
  3. Raw transcription is injected into the currently active window (e.g., Notepad).
**Plans**: 2 plans

Plans:
- [x] 02-01: Faster-Whisper integration and model loading logic.
- [x] 02-02: Global hotkey and system-wide keyboard injection.

### Phase 3: AI Polisher (Grammar API)
**Goal**: Transform raw speech into "polished" text using the Gemini 3 Flash API.
**Depends on**: Phase 2
**Requirements**: GRAM-01, GRAM-02, GRAM-03, INJS-03
**Success Criteria**:
  1. Raw text is sent to Gemini and returned with correct punctuation and grammar.
  2. System uses an internal buffer to process full thoughts/sentences before "flashing" the result.
  3. Polished text replacement is atomic (fast injection) to avoid racing with the user's hands.
**Plans**: 2 plans

Plans:
- [ ] 03-01: Gemini API client and sentence-buffering logic.
- [ ] 03-02: Polished text injection and replacement strategy.

### Phase 4: Technical Presets (Coding Mode)
**Goal**: Enable specialized "technical" mode to ensure IDE-compatibility.
**Depends on**: Phase 3
**Requirements**: GRAM-04, INJS-04
**Success Criteria**:
  1. Technical vocabulary (e.g., `git push`, `camelCase`) is preserved by the AI layer.
  2. User can toggle between "Standard" and "Technical" polishing modes.
  3. System identifies focus shifts and avoids injecting into windows that changed mid-processing.
**Plans**: 1 plan

Plans:
- [ ] 04-01: Advanced system prompting and context-aware filtering.

### Phase 5: Wake Word ("Vox") Triggering
**Goal**: Add hands-free "Vox" activation using the openWakeWord engine.
**Depends on**: Phase 2
**Requirements**: AUST-03
**Success Criteria**:
  1. Background listener detects "Vox" wake word with high accuracy and low CPU usage.
  2. Detecting the wake word triggers the Phase 2 recording loop.
**Plans**: 1 plan

Plans:
- [ ] 05-01: openWakeWord integration and background listener thread.

### Phase 6: Visual Feedback & UI
**Goal**: Provide a lightweight desktop interface for status and configuration.
**Depends on**: Phase 4, Phase 5
**Requirements**: UICO-01, UICO-02, UICO-03, AUST-04
**Success Criteria**:
  1. System tray icon displays the current app state (Idle vs Recording).
  2. A subtle "Status Overlay" appears on screen during active listening/polishing.
  3. Settings window allows customization of hotkeys and AI parameters.
**Plans**: 2 plans

Plans:
- [ ] 06-01: PyQt6 System Tray and Status Overlay implementation.
- [ ] 06-02: Settings management and UI refinement.

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Setup & Audio | 0/2 | Not started | - |
| 2. STT & Hotkeys | 0/2 | Not started | - |
| 3. AI Polisher | 0/2 | Not started | - |
| 4. Technical Presets | 0/1 | Not started | - |
| 5. Wake Word | 0/1 | Not started | - |
| 6. Visuals & UI | 0/2 | Not started | - |

---
*Roadmap defined: 2026-03-22*
