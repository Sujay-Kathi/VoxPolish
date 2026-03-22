# Implementation Plan: VoxPolish Native Desktop (.exe)

**Task:** Transform VoxPolish into a high-fidelity, native Windows application (.exe) with a Wispr Flow-inspired interface.

## 🛠 Tech Stack
- **Core**: Python 3.10+
- **UI Framework**: PyQt6 (Native widgets, custom painting for Glassmorphism)
- **Packaging**: PyInstaller (.exe)
- **Design Reference**: Stitch project 'VoxPolish Floating UI' (Aetheric Flux System)

---

## 🏗 Phase 2 Orchestration Strategy (Sequential implementation)

### 1. UI Architecture (`frontend-specialist`)
- **FloatingWedge**: Create a frameless, transparent `QWidget` pinned to the bottom center.
- **Glassmorphism Engine**: Implement a custom `paintEvent` to handle the 'frosted glass' blur and cyan luminous glow.
- **Pulse Animation**: Use `QPropertyAnimation` for the microphone state (Listening/Idle).

### 2. Core Logic Integration (`backend-specialist`)
- **Thread Management**: Decouple the `AudioCollector` and `WhisperSTT` from the main UI thread.
- **State Signals**: Update the Wedge via PyQt signals (Listening -> Thinking -> Success).
- **Injection Logic**: Refine the `keyboard` injection to ensure compatibility with IDEs.

### 3. Packaging & Distribution (`devops-engineer`)
- **Spec File**: Create a robust `.spec` file for PyInstaller to bundle dependencies (sounddevice DLLs, weights, etc.).
- **Build Script**: `python scripts/build_exe.py` to automate the .exe generation.

---

## 📋 Task Breakdown

### Wave 1: Foundation & The Wedge
- [ ] Implement `VoxWedgeUI` (The bottom floating pill).
- [ ] Add `Coding Mode` toggle icon (Terminal).
- [ ] Add `Settings` icon.
- [ ] Implement the "Hover Expansion" effect.

### Wave 2: Animation & Feedback
- [ ] Implement the 'Luminous Pulse' for active listening.
- [ ] Add the floating 'Transcription Preview' label that appears above the wedge.
- [ ] Implement the 'Success' flash (Green glow).

### Wave 3: Native Dashboard
- [ ] Create the Main Window (Dashboard) for history and settings.
- [ ] Use `QScrollArea` for the transcription log with glass-styled cards.

### Wave 4: Packaging
- [ ] Configure `PyInstaller` to handle `ctranslate2` and `webrtcvad` binaries.
- [ ] Generate `VoxPolish.exe`.

---

## 🧪 Verification Criteria
- **UICO-04**: Wedge appears at the bottom center, stays on top of all windows.
- **AUST-05**: Clicking the mic or using Win+Shift+V triggers 'Listening' state.
- **DIST-01**: Application can be bundled into a functional .exe without requiring a Python environment on the host.

---

## ⏹ Socratic Gate (Pre-Approval Questions)
1. **Packaging**: Do you want a single-file `.exe` (slower startup) or a directory-based bundle (standard for bigger apps)?
2. **Persistence**: Should the transcription history be stored in a local SQLite database or a simple JSON file?
3. **Icons**: Do you have specific SVG icons you'd like to use for the mic/gear, or should I generate/use standard Lucide-style paths?
