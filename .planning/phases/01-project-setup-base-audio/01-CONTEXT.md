# Phase 1: Project Setup & Base Audio - Context

**Gathered:** 2026-03-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Set up the project structure, development environment, and core audio capture module.
Includes:
- Virtual environment (`venv`) and dependency file (`requirements.txt`).
- A modular project layout under `voxpolish/core`.
- High-efficiency, multi-threaded audio capture using `sounddevice` and `webrtcvad`.

</domain>

<decisions>
## Implementation Decisions

### Environment & Tooling
- **D-01:** Use standard Python `venv` for environment isolation.
- **D-02:** Use Python 3.11 as the base version.
- **D-03:** Manage dependencies via `requirements.txt`.

### Project Architecture
- **D-04:** Modular codebase centered in `voxpolish/core`.
- **D-05:** Sub-modules for `audio`, `stt`, and `grammar` will reside within `voxpolish/core/`.

### Audio Pipeline
- **D-06:** Use `sounddevice` for low-latency, cross-platform audio input.
- **D-07:** Implement `webrtcvad` for lightweight, fast Voice Activity Detection (VAD).
- **D-08:** Adopt a Producer-Consumer threading model where one thread records to a queue and a consumer thread handles logic.
- **D-09:** Recording triggers and stop conditions are driven by dynamic VAD signals (silence detection).

### the agent's Discretion
- Library-specific wrapper names (e.g., `voxpolish/core/audio.py` or similar).
- Buffer size optimizations (e.g., 20ms chunks required by webrtcvad).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project Core
- `.planning/PROJECT.md` — Project vision and non-negotiables.
- `.planning/REQUIREMENTS.md` — Acceptance criteria for AUST-01.
- `.planning/ROADMAP.md` — Phase goal and success criteria for Phase 1.

### Technical Stack
- `.planning/research/STACK.md` — Recommended versions and library patterns.
- `.planning/research/ARCHITECTURE.md` — System-wide threading/data-flow model.

</canonical_refs>

<specifics>
## Specific Ideas
- Focus on minimizing CPU usage during audio capture, especially the VAD overhead.
- Ensure the audio capture thread can be gracefully stopped and restarted for testing.

</specifics>

<deferred>
## Deferred Ideas
- AI-based VAD (more complex, but heavier on CPU) is deferred unless webrtcvad fails to deliver.
- GUI for status feedback (Phase 6).
- Hotkey integration (Phase 2).

</deferred>

---

*Phase: 01-project-setup-base-audio*
*Context gathered: 2026-03-22 via adaptive discussion*
