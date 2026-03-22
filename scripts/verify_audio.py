import os
import sys
import time

# Add the project root to sys.path for importing voxpolish
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from voxpolish.core.audio import AudioCollector

def main():
    print("--- VoxPolish Audio Verification ---")
    
    collector = AudioCollector(vad_aggressiveness=3)
    
    # 1. Start recording
    try:
        collector.start()
        print("Listening for 5 seconds... say something!")
        
        # 2. Check for speech/silence during this time
        for i in range(5):
            time.sleep(1)
            buf_len = len(collector.speech_buffer)
            print(f"Elapsed: {i+1}s | Speech Frames Buffered: {buf_len}")
            
    except Exception as e:
        print(f"Error during recording: {e}")
        
    finally:
        # 3. Stop
        collector.stop()
        final_buf = collector.get_captured_audio()
        print(f"Total Captured Speech Samples: {len(final_buf)}")
        
        if len(final_buf) > 0:
            print("Verification: SUCCESS (Audio data received)")
        else:
            print("Verification: PARTIAL (No speech detected - check mic or speak louder!)")
            
    print("Verification script complete.")

if __name__ == "__main__":
    main()
