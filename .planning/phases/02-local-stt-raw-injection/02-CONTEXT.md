# Phase 2: Local STT & Raw Injection - Context

**Gathered:** 2026-03-22
**Status:** Ready for planning

<domain>
## Phase Boundary

Implement the local Speech-to-Text (STT) layer and global OS integration.
Includes:
- STT Module using `faster-whisper` (tiny.en).
- Global keyboard injection and hotkey handling (`keyboard` or `pynput`).
- Audio-STT bridge (STT processes the speech buffer from Phase 1).

</domain>

<decisions>
## Implementation Decisions

### STT Configuration
- **D-10:** Use `faster-whisper` with the `tiny.en` model for maximum speed and minimum resource usage.
- **D-11:** Implement silence trimming (tail-end clipping) before sending audio to STT to reduce latency.

### OS Integration
- **D-12:** Default hotkey is **`Ctrl + Alt + Z`** to toggle recording.
- **D-13:** Hotkey configuration should be handled via a simple `config.json` file in the project directory, allowing for future user editability.
- **D-14:** Injection mode: The system should "type" the transcription into the active cursor without a following "Enter" or submit signal.

### Technical Patterns
- **D-15:** STT processing should be asynchronous to avoid blocking the audio capture thread.
- **D-16:** Use a dedicated `voxpolish/core/stt.py` module for STT abstraction.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

- `.planning/phases/01-project-setup-base-audio/01-VERIFICATION.md` — To ensure audio capture is stable.
- `voxpolish/core/audio.py` — The interface for the speech buffer.

</canonical_refs>

<specifics>
## Specific Ideas
- The STT engine should be initialized once at startup to avoid "cold start" latency during first use.
- Use the `ctranslate2` version (faster-whisper) which is optimized for CPU/low-spec.

</specifics>

<deferred>
## Deferred Ideas
- Grammar correction (Phase 3).
- Technical vocabulary presets (Phase 4).
- GUI for editing hotkeys (Phase 6).

</deferred>

---

*Phase: 02-local-stt-raw-injection*
*Context gathered: 2026-03-22 via adaptive discussion*
