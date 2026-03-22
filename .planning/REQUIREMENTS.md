# Requirements: VoxPolish

**Defined:** 2026-03-22
**Core Value:** Turn spoken ideas into perfectly formatted text in any application, with zero latency and zero cost to the user.

## v1 Requirements

### Audio & STT (AUST)

- [ ] **AUST-01**: User can record audio from the default system microphone.
- [ ] **AUST-02**: System transcribes audio locally using Faster-Whisper (tiny.en/base.en).
- [ ] **AUST-03**: Transcription happens only when triggered (via hotkey or wake word).
- [ ] **AUST-04**: System automatically detects silence to stop recording.

### Grammar & AI (GRAM)

- [ ] **GRAM-01**: System sends raw transcription to Gemini 3 Flash API for polishing.
- [ ] **GRAM-02**: System adds appropriate punctuation (periods, commas, question marks).
- [ ] **GRAM-03**: AI polishes grammar into a professional, clear style.
- [ ] **GRAM-04**: AI preserves technical vocabulary and case sensitivity (e.g., camelCase, git commands).

### Injection & OS (INJS)

- [ ] **INJS-01**: System-wide global hotkey (e.g., Win+Shift+V) to start/stop listening.
- [ ] **INJS-02**: System injects polished text into the currently active window.
- [ ] **INJS-03**: Injection is atomic (using clipboard or fast typing) to prevent race conditions.
- [ ] **INJS-04**: System handles focus shifts gracefully by buffering text if the target app changes.

### UI & Controls (UICO)

- [ ] **UICO-01**: System tray icon for app status (Idle, Recording, Processing).
- [ ] **UICO-02**: Visual overlay (small indicator) to show the user that the app is "heard" and "polishing".
- [ ] **UICO-03**: Settings menu to configure Hotkeys, Models, and technical presets.

## v2 Requirements

### Advanced Features

- **ADVF-01**: Multi-language support (Spanish, French, etc.).
- **ADVF-02**: Voice commands for formatting (e.g., "new paragraph", "bullet point").
- **ADVF-03**: Integration with local LLAMA.cpp for a 100% offline "Pro" mode.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Browser Extension | System-wide desktop app is more universal for IDE/Email/Doc use. |
| Streaming Real-time Correction | Sentence-level "flash" provides better grammar context and lower UI flicker. |
| User Accounts/Sync | Zero-cost goal favors local-first, anonymous usage. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| AUST-01 | Phase 1 | Pending |
| AUST-02 | Phase 1 | Pending |
| AUST-03 | Phase 1 | Pending |
| INJS-01 | Phase 1 | Pending |
| INJS-02 | Phase 1 | Pending |
| GRAM-01 | Phase 2 | Pending |
| GRAM-02 | Phase 2 | Pending |
| GRAM-03 | Phase 2 | Pending |
| INJS-03 | Phase 2 | Pending |
| GRAM-04 | Phase 3 | Pending |
| INJS-04 | Phase 3 | Pending |
| UICO-01 | Phase 4 | Pending |
| UICO-02 | Phase 4 | Pending |
| UICO-03 | Phase 4 | Pending |
| AUST-04 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-22*
*Last updated: 2026-03-22 after initial definition*
