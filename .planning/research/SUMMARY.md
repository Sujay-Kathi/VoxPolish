# Project Research Summary

**Project:** VoxPolish
**Domain:** Desktop Speech-to-Text Utility
**Researched:** 2026-03-22
**Confidence:** HIGH

## Executive Summary

VoxPolish is designed to bridge the gap between spoken thoughts and professional, typed text. By combining high-efficiency, local STT (Faster-Whisper) with state-of-the-art grammar polishing (Gemini 3 Flash), we can deliver a tool that offers both privacy and unmatched intelligence for technical and casual writing.

The recommended approach centers on a lightweight Python-based desktop application. It avoids the heavy resource footprint of Electron, ensuring compatibility with any PC spec. By prioritizing sentence-based "flash" injection over word-by-word streaming, we achieve higher accuracy and superior grammar context without being distracting to the user's flow.

## Key Findings

### Recommended Stack

- **Python 3.11** as the orchestration layer for its deep OS-level library support and ML hooks.
- **Faster-Whisper** as the local transcription engine for its 4x performance boost over original Whisper, specifically optimized for CPU usage on low-spec systems.
- **Gemini 3 Flash (via Google AI Studio)** for zero-cost, high-speed grammar and punctuation correction.
- **PyQt6** for a performant, non-blocking desktop user interface.

### Expected Features

- **Global Hotkey & Wake Word ("Vox")** for hands-free or one-click triggering.
- **Sentencing & Polishing** to transform spoken ideas into punctuated, professional text.
- **Technical Vocab Support** to prevent the AI from incorrectly "fixing" code, camelCase, or technical terms in IDEs.
- **System-Wide Injection** that works across IDEs (Antigravity), browsers, and documents.

### Architecture Approach

A **Producer-Consumer multi-threaded model** is essential to prevent UI stalls and ensure zero audio loss during transcription. The audio is captured in chunks, transcribed locally, then polished by the Gemini API before being "pasted" or typed into the active window.

### Critical Pitfalls

1. **Wait-and-Flash Latency**: If transcription/polishing takes more than 2 seconds, the flow breaks. We mitigate this with Whisper-tiny and Gemini-Flash.
2. **Grammar Over-Correction**: LLMs may break code syntax; this is solved with specialized technical system prompts.
3. **Admin Permissions**: Global injection requires admin rights on many Windows systems.

## Implications for Roadmap

Suggested phase structure:

### Phase 1: Core Transcription & Hotkeys
**Rationale:** Establishes the fundamental loop (Record -> Transcribe -> Inject) without the complexity of grammar polishing.
**Delivers:** Local hotkey activation and raw STT injection into active windows.

### Phase 2: AI Polishing (The "VoxPolish" Layer)
**Rationale:** Introduces the differentiator — grammar, and punctuation via the Gemini API.
**Delivers:** Professional text-polishing logic and sentence-level "flash" injection.

### Phase 3: Technical Customization
**Rationale:** Addresses the "IDE Prompting" requirement by fine-tuning the AI layer for code conservation.
**Delivers:** Technical presets and code-friendly grammar prompts.

### Phase 4: Hands-Free & Polish
**Rationale:** Adds high-value convenience features and visual refinements once the core loop is robust.
**Delivers:** Wake word detection and a visual status overlay for the desktop.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Verified library performance on low-resource hardware. |
| Features | HIGH | Aligns perfectly with the user's initial core request. |
| Architecture | HIGH | Proven patterns for real-time STT systems. |
| Pitfalls | MEDIUM | Keyboard injection in complex IDEs can be unpredictable; needs testing. |

**Overall confidence:** HIGH

## Sources

- Official docs for Faster-Whisper, Gemini 1.5/2 API, openWakeWord.
- Python Keyboard Injection benchmarks on Windows.

---
*Research completed: 2026-03-22*
*Ready for roadmap: yes*
