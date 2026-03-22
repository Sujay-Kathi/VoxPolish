# Phase 1: Project Setup & Base Audio - Validation Strategy

**Phase:** 01
**Slug:** project-setup-base-audio
**Defined:** 2026-03-22

## Validation Objective
To ensure that the "Base Audio" (AUST-01) is robust and that the `Producer-Consumer` model is correctly implemented.

## Dimension 8: Validation Architecture

### Audio Check
- [ ] **CH-01: Microhpone Presence** — System detects at least one audio input device.
- [ ] **CH-02: RMS Level Check** — Verify that audio data contains varying amplitude (not flatline/silence).

### Threading & Queue
- [ ] **TQ-01: No Data Loss** — Producer-Consumer queue remains healthy under heavy load; no frames are dropped.
- [ ] **TQ-02: Graceful Termination** — Audio recording thread stops cleanly when the "stop" signal is issued.

### Modular Structure
- [ ] **MS-01: Sub-module Imports** — `voxpolish.core.audio` can be imported without errors in a clean `venv`.

## Verification Methods

### Automated Tests
- Running `pytest tests/test_audio.py` — specifically testing the threading logic.
- Verifying `voxpolish/core/audio.py` for correct `sounddevice` usage.

### Manual Verification
- Run a standalone test script that records 5 seconds of audio and prints RMS levels.
- Test with different `webrtcvad` aggressiveness levels (0-3).

---
*Validation strategy for Phase 1.*
