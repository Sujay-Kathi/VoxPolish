import os
import subprocess
import shutil

def build():
    print("🚀 Starting VoxPolish Build Process...")
    
    # 1. Clean previous builds
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            
    # 2. PyInstaller command
    # We use --onedir for stability as it's a complex app
    # We include assets/icons folder
    # We include .env for API keys (or we should ask to create it, but for local use we bundle it)
    
    command = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "VoxPolish",
        "--add-data", f"voxpolish/assets{os.pathsep}voxpolish/assets",
        "--add-data", f".env{os.pathsep}.",
        "--hidden-import", "PyQt6.QtSvg",
        "main.py"
    ]
    
    print(f"Running: {' '.join(command)}")
    subprocess.run(command)
    
    print("\n✅ Build Complete! Check the 'dist/VoxPolish' folder.")

if __name__ == "__main__":
    build()
