# Feature Research

**Domain:** Desktop Speech-to-Text Utility
**Researched:** 2026-03-22
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Accurate Transcription | Primary purpose of the app. | MEDIUM | Whisper models provide human-parity accuracy. |
| Global Hotkeys | Quick activation without task-switching. | LOW | Essential for IDE use. |
| Automatic Punctuation | Unpunctuated speech is hard to read. | MEDIUM | Handled by Gemini or Whisper's built-in VAD. |
| Low Latency | User wants to see text "flash" quickly. | HIGH | Proper buffering required. |

### Differentiators (Competitive Advantage)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Grammar Transformation | Polishes speech into professional prose. | MEDIUM | Gemini 3 Flash allows for stylistic prompt control. |
| Technical Vocab Support | Prevents "fixing" code/technical terms. | HIGH | Needs specialized prompt instructions for the LLM. |
| Wake Word ("Vox") | Hands-free operation for long sessions. | MEDIUM | Better flow for document/email writing. |
| Zero Subscription Cost | No monthly fees unlike competitors. | LOW | Key architectural constraint. |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Real-Time Streaming | Instant gratification. | Fragmentation and lower grammar quality. | Sentence-level "flash" (buffered correction). |
| Multi-Cloud Sync | Cross-device history. | Data privacy and cost/latency. | Local history or single cloud provider. |
| Real-time Translation | For cross-border work. | Too much latency and cost for MVP. | Add as a separate mode later. |

## Feature Dependencies

```
[Audio Capture]
    └──requires──> [Whisper Engine]
                        └──requires──> [Gemini Polishing]
                                             └──produces──> [Keyboard Injection]

[Wake Word Listener] ──activates──> [Audio Capture]
[Global Hotkey] ──activates──> [Audio Capture]
```

### Dependency Notes

- **Whisper -> Gemini:** Polishing requires fixed-block text (sentences) to provide accurate grammar context.
- **Injection -> Window Focus:** Injection requires the target application to handle input events properly.

## MVP Definition

### Launch With (v1)

- [ ] **Hotkey STT**: Press key -> Record -> Transcribe -> Inject.
- [ ] **Basic Punctuation**: Automatic period/comma addition via Whisper.
- [ ] **Grammar Correction**: Basic polish via Gemini Flash API.
- [ ] **Windows Injection**: Reliable text typing into any active window.

### Add After Validation (v1.x)

- [ ] **Wake Word ("Vox")**: Hands-free triggering.
- [ ] **Coding Preset**: Mode to preserve technical terms.
- [ ] **UI Monitor**: Visual indicator of listening state (overlay/tray info).

### Future Consideration (v2+)

- [ ] **Custom Style Presets**: "Email Mode", "Prompt Mode", "Technical Document Mode".
- [ ] **Local LLM Option**: Fully offline version for high-spec machines.

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| STT Accuracy | HIGH | MEDIUM | P1 |
| Text Injection | HIGH | LOW | P1 |
| Basic Grammar | MEDIUM | MEDIUM | P1 |
| Global Hotkey | HIGH | LOW | P1 |
| Technical Vocab | HIGH | HIGH | P2 |
| Wake Word | MEDIUM | MEDIUM | P2 |

## Competitor Feature Analysis

| Feature | Nuance (Paid) | VS Code Speech (Limited) | Our Approach |
|---------|---------------|--------------------------|--------------|
| Technical Focus | Weak | Standard | Strong (Gemini-powered) |
| System-Wide | Yes | No | Yes (Keyboard injection) |
| Cost | Expensive ($300+) | Free (with IDE) | Zero (with API key) |

## Sources

- Nuance Communications — Standard for enterprise STT feature sets.
- Whisper GitHub Community — Features requested by open-source users.
- Gemini API Technical Reference — Capabilities for grammar and context handling.

---
*Feature research for: Desktop Speech-to-Text Utility*
*Researched: 2026-03-22*
