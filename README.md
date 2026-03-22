# 🎙️ VoxPolish: Speak. Polish. Write. ✨

**VoxPolish** is your personal voice-activated AI writing companion. It transforms your raw speech into grammatically perfect, professional text and pastes it instantly into whatever application you are using. Whether you're writing an email, a document, or code, just speak your thoughts and let the AI handle the rest.

---

## 🚀 Awesome Features

- 🎧 **Wake Word Detection**: Start recording just by saying *"Hey Vox"* or *"Alexa"* or *"Hey Jarvis"*.
- 🎹 **Global Hotkeys**: 
  - `Ctrl + Alt + Z`: Basic polishing for emails and chats.
  - `Ctrl + Alt + C`: Special **Coding Mode** for technical documentation and code comments.
- ⚡ **Instant Paste**: Automatically types the polished text into your active window.
- ☁️ **Hybrid STT Intelligence**: Uses a combination of local **Whisper** and cloud-based **Gemini AI** for lightning-fast, high-accuracy transcription.
- 🛠️ **Seamless Integration**: Works anywhere! Slack, Discord, Visual Studio Code, Gmail, or even Notepad.
- 🌈 **Minimal Wedge UI**: A sleek, non-intrusive UI that keeps you focused while providing real-time status updates.

---

## 🛠️ Local Installation Guide

Follow these steps to get **VoxPolish** running on your local machine:

### 1. Prerequisites
- **Python 3.10+** (Ensure you have Python installed and added to your PATH).
- **FFmpeg**: Required for audio processing. You can install it on Windows via [Chocolatey](https://chocolatey.org/): `choco install ffmpeg`.

### 2. Clone the Repository
```bash
git clone https://github.com/yourusername/voxpolish.git
cd voxpolish
```

### 3. Run the Setup Script
We’ve made it easy for you! Just run the included PowerShell setup script:
```powershell
./setup.ps1
```
*This will create a virtual environment and install all necessary dependencies.*

---

## 🔑 Environment Setup (`.env`)

To power the AI polishing, you will need a **Google Gemini API Key**.

1. Copy the example file to a new file named `.env`:
   ```bash
   copy .env.example .env
   ```
2. Open `.env` and enter your API key:
   ```env
   GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
   ```
   > 💡 **Get your key!** You can generate a free Gemini API key at the [Google AI Studio](https://aistudio.google.com/).

---

## 🏃 How to Run VoxPolish

### **Method 1: Run as a Python Script**
Activate your virtual environment and launch the app:
```powershell
.\venv\Scripts\Activate.ps1
python main.py
```

### **Method 2: Run the Executable (.exe)**
If you have a binary build, go to the `dist/VoxPolish/` folder and double-click `VoxPolish.exe`.

---

## 📦 Building the Executable

If you want to package VoxPolish into a standalone `.exe` for distribution without needing Python installed on other machines, use the following commands:

### **Option 1: Using our Build Script (Recommended)**
We provide a Python script that handles all the heavy lifting (cleaning, assets, paths):
```bash
python scripts/build_exe.py
```

### **Option 2: Manual PyInstaller Command**
If you prefer to run it manually:
1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```
2. **Build with the Spec file:**
   ```bash
   pyinstaller --noconfirm VoxPolish.spec
   ```
3. **Locate your App:**
   After building, your ready-to-use software will be in the `dist/VoxPolish/` directory. Double-click `VoxPolish.exe` to launch.

---

## 🎮 How to Use

1. **Start the App:** Once active, you'll see a small wedge UI.
2. **Speak:** Say *"Hey Alexa"* (or use your hotkey) and say what's on your mind.
3. **Wait a Blink:** The UI will pulse as it polishes your speech.
4. **Boom!** The polished text is typed automatically into your active application.

---

## 🤝 Contributing
Feel free to fork this repo, open issues, or submit PRs! Let's make writing effortless for everyone. 🌟

---

*Made with ❤️ for faster, better writing.*

---

### ✨ Created by **Sujay Kathi** 🚀
# VoxPolish
