# Pitfalls Research

**Domain:** Desktop Speech-to-Text Utility
**Researched:** 2026-03-22
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: Technical Vocabulary Destruction (Autocorrect)

**What goes wrong:**
The grammar AI "corrects" valid code or technical terms into standard English (e.g., `git merge` becomes "get merge" or `CamelCase` becomes "Camel case").

**Why it happens:**
LLMs are trained predominantly on natural language; they default to fixing "errors" that are actually intentional technical terms.

**How to avoid:**
Use specialized system prompts in the grammar layer: "You are a technical assistant; preserve code-related terms, case sensitivity, and technical keywords."

**Warning signs:**
User starts manually fixing the "corrected" text in their IDE.

**Phase to address:**
Phase 3: Grammar & AI Customization.

---

### Pitfall 2: High Latency in "Flash" Injection

**What goes wrong:**
The time between finishing a sentence and the polished text appearing in the IDE is >2 seconds, breaking the user's flow.

**Why it happens:**
STT processing + API roundtrip + injection simulation time adds up on low-spec hardware.

**How to avoid:**
Use `Faster-Whisper` with `tiny.en` model (optimized for speed) and Gemini 3 Flash (optimized for low-latency response).

**Warning signs:**
User starts typing before the voice text appears, causing "jumbled" input.

**Phase to address:**
Phase 2: Core STT & API Integration.

---

### Pitfall 3: Keyboard Injection Race Conditions

**What goes wrong:**
Text is injected while the user is also typing, or the focus switches mid-injection, sending text to the wrong window.

**Why it happens:**
System-wide hooks are asynchronous and don't "block" the user's manual keyboard.

**How to avoid:**
Briefly disable injection or use the clipboard for large blocks to ensure atomic "paste" performance.

**Warning signs:**
Missing characters or text appearing in the wrong application.

**Phase to address:**
Phase 4: OS Integration & Window Handling.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Skipping Wake Word | Faster MVP dev. | Higher friction for the user (always needs hotkey). | MVP Stage (Phase 1). |
| Hardcoded STT Path | Easier file handling. | Fails if user moves the app. | Only during internal prototyping. |
| Basic String Injection | Simplest code. | Jumbled text in complex IDEs. | Until Phase 4 is reached. |

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Gemini API | Sending raw audio. | Always transcribe locally first then send text (saves egress/tokens). |
| Windows Tray | Heavy UI frameworks. | Use PyQt6/PySide for native, light tray feel. |
| Keyboard Library | Missing Admin perms. | Prompt user to "Run as Administrator" if injection fails. |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Large Whisper Model | >100% CPU usage. | Use `tiny.en` or `base.en`. | Always on low-spec PCs. |
| Blocking Main Thread | UI freeze during AI call. | Move STT/LLM to background threads. | During any long sentence. |
| Excessive API Calls | Gemini Rate Limiting errors. | Buffer at least 1-2 sentences. | If user talks without breathing. |

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| API Key Exposure | Key stolen from public repo. | Use `.env` files or system keychain. |
| Logging Audio | Private data leak. | Audio should never be written to disk permanently. |
| Hijacking Keys | Disabling critical OS keys. | Only hook specific, unusual combinations. |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| "Phantom" Injection | Text appears out of nowhere. | Use a subtle overlay (indicator) to show "Polishing..." state. |
| Unmapped Commands | Commands like "new paragraph" are literal. | Implement basic "Natural Language Command" parsing. |

## "Looks Done But Isn't" Checklist

- [ ] **STT:** Often missing Silence Detection — verify it stops recording automatically.
- [ ] **Injection:** Often fails in VS Code terminal — verify terminal shell compatibility.
- [ ] **API:** Often fails on low internet — verify timeout handling for Gemini calls.

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| API Timeout | MEDIUM | Flash back the "Raw" transcription without grammar polish. |
| Focus Loss | LOW | Buffer the text and show an "Injection Failed" notification. |

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Technical Vocab | Phase 3 | Test with `camelCase` and `snake_case` keywords. |
| High Latency | Phase 2 | Measure "Stop-to-Screen" time (<1.5s benchmark). |
| Injection Race | Phase 4 | Try to type manually while voice is being injected. |

## Sources

- Common issues with Python `keyboard` library on GitHub.
- Experience building low-spec speech utilities.

---
*Pitfalls research for: Desktop Speech-to-Text Utility*
*Researched: 2026-03-22*
