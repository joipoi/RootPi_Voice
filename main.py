# main.py
import os
import time
from datetime import datetime
import webrtcvad

from recording import Recorder

# --- PARAMETERS ---
SAMPLE_RATE = 16000
FRAME_DURATION_MS = 30       # frame must be either 10, 20, or 30 ms
VAD_AGGRESSIVENESS = 3       # 0=least strict, 3=most strict
SILENCE_DURATION_MS = 1000   # Stop recording after ~1 sec of silence
OUTPUT_DIR = "recordings"

# Ensure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    # Initialize VAD
    vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)

    # Initialize Recorder
    recorder = Recorder(sample_rate=SAMPLE_RATE, frame_duration_ms=FRAME_DURATION_MS)
    recorder.start_stream()
    print("Listening for speech... Press Ctrl+C to stop.")

    # State machine
    STATE_IDLE = 0
    STATE_RECORDING = 1
    state = STATE_IDLE

    silence_frames = int(SILENCE_DURATION_MS / FRAME_DURATION_MS)

    consecutive_silence = 0

    try:
        for frame in recorder.frames():
            is_speech = vad.is_speech(frame.bytes, SAMPLE_RATE)

            if state == STATE_IDLE:
                if is_speech:
                    # Start recording
                    state = STATE_RECORDING
                    recorder.start_recording()
                    recorder.buffer_frame(frame)
                    consecutive_silence = 0
                    print(f"Speech detected! Recording started at {datetime.now().strftime('%H:%M:%S')}")

            elif state == STATE_RECORDING:
                recorder.buffer_frame(frame)
                if is_speech:
                    consecutive_silence = 0
                else:
                    consecutive_silence += 1
                    if consecutive_silence >= silence_frames:
                        # Stop recording
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = os.path.join(OUTPUT_DIR, f"recording_{timestamp}.wav")
                        recorder.save_recording(filename)
                        state = STATE_IDLE
                        consecutive_silence = 0
                        print("Waiting for next speech segment...")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        recorder.stop_stream()

if __name__ == "__main__":
    main()
