# VoxPolish (v1.0 Shipped) 🎙️✨

## What This Is

VoxPolish is a system-wide desktop application that provides high-accuracy speech-to-text (STT) transcription with integrated real-time grammar and punctuation correction. Designed for professional use in IDEs, document editors, and email clients, it polishes spoken thoughts into structured, well-formatted text.

## Core Value

Turn spoken ideas into perfectly formatted text in any application, with zero latency and zero cost to the user.

## Requirements

### Validated

- **AUST-01**: Robust multi-threaded audio capture pipeline using `sounddevice` and `webrtcvad`. (Validated in Phase 01: Project Setup & Base Audio)


### Active

- [ ] **System-Wide Desktop App**: A background utility that can inject text into any active window.
- [ ] **STT Engine**: Implementation of a high-efficiency STT model (e.g., Whisper-tiny or similar) to ensure low-spec compatibility.
- [ ] **Sentence-Based Correction**: Transcribe full thoughts/sentences and "flash" the polished version to ensure context-aware grammar.
- [ ] **Grammar & Punctuation Layer**: An AI-driven correction layer using free-tier APIs (like Gemini Free Tier) or optimized local LLMs.
- [ ] **Technical Vocabulary Support**: Specialized handling for coding and technical terms to prevent improper "autocorrect" in IDEs.
- [ ] **No-Cost Guarantee**: Built using open-source models and free-tier APIs to ensure no running costs for the user.
- [ ] **Triggering Mechanism**: Support for both global **hotkeys** (e.g., Win+Shift+V) and a **wake word** (e.g., "Vox") to start/stop listening.

### Out of Scope

- [ ] **Browser Extension**: A standalone extension is deferred in favor of a universal system-wide desktop approach.
- [ ] **Real-Time Word-by-Word Correction**: Sentence-level correction is prioritized for architectural simplicity and grammar accuracy.
- [ ] **Heavy-Duty Local LLMs**: Large models requiring high-end GPUs are excluded to maintain compatibility with low-spec hardware.

## Context

- The user wants to use this for "prompting in Antigravity or any IDE," "document writing," and "email writing."
- Modern IDEs often have unique keyboard handling; the injection mechanism must be robust.
- "No cost" and "low spec" are the primary architectural constraints.

## Constraints

- **Budget**: Zero cost — must use free-tier APIs (Gemini) or lightweight open-source models.
- **Performance**: High Efficiency — must run on lower-end hardware without significant lag.
- **Compatibility**: Desktop environment — initially targeting Windows as per user environment.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Desktop App | System-wide reach into IDEs/Email/Docs | — Validated |
| Modular Core | voxpolish/core structure for STT/Grammar/Audio separation | — Validated |
| sounddevice + webrtcvad | Optimal for low-latency, low-spec silence detection | — Validated |
| Producer-Consumer Threading | Zero-loss audio capture with asynchronous processing | — Validated |


## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-22 after Phase 01 completion.*
