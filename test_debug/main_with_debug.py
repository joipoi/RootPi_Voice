# test_debug/test_vad_stream.py
import os
import time
from datetime import datetime
from collections import deque
import webrtcvad
import numpy as np
import csv

from recording import Recorder, Frame

# --- PARAMETERS ---
SAMPLE_RATE = 16000
FRAME_DURATION_MS = 30
VAD_AGGRESSIVENESS = 3
PREBUFFER_DURATION_MS = 500
VALIDATION_FRAMES = 5
SILENCE_DURATION_MS = 1000
DEBUG = True

OUTPUT_DIR = "recordings"
LOG_DIR = "test_debug/debug_logs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --- UTILITY ---
def frame_rms(frame):
    """Compute RMS volume of a frame."""
    samples = np.frombuffer(frame.bytes, dtype=np.int16).astype(np.float32)
    rms = np.sqrt(np.mean(samples**2)) / 32768.0  # normalize
    return rms

# --- MAIN ---
def main():
    vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)
    recorder = Recorder(sample_rate=SAMPLE_RATE, frame_duration_ms=FRAME_DURATION_MS)
    recorder.start_stream()
    print("DEBUG: Listening for speech... Press Ctrl+C to stop.")

    STATE_IDLE = 0
    STATE_RECORDING = 1
    state = STATE_IDLE

    silence_frames = int(SILENCE_DURATION_MS / FRAME_DURATION_MS)
    prebuffer_frames = int(PREBUFFER_DURATION_MS / FRAME_DURATION_MS)

    consecutive_silence = 0
    consecutive_voiced = 0
    prebuffer = deque(maxlen=prebuffer_frames)

    # Open CSV log
    log_file = os.path.join(LOG_DIR, f"debug_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    with open(log_file, 'w', newline='') as csvfile:
        logwriter = csv.writer(csvfile)
        logwriter.writerow(['frame', 'timestamp', 'VAD', 'RMS', 'state'])

        frame_count = 0
        try:
            for frame in recorder.frames():
                frame_count += 1
                is_speech = vad.is_speech(frame.bytes, SAMPLE_RATE)
                rms = frame_rms(frame)
                prebuffer.append(frame)

                # Log current frame
                logwriter.writerow([frame_count, round(frame.timestamp, 3), int(is_speech), round(rms, 5), state])

                # --- State machine with pre-buffer + validation ---
                if state == STATE_IDLE:
                    if is_speech:
                        consecutive_voiced += 1
                        if consecutive_voiced >= VALIDATION_FRAMES:
                            state = STATE_RECORDING
                            recorder.start_recording()
                            for f in prebuffer:
                                recorder.buffer_frame(f)
                            prebuffer.clear()
                            consecutive_silence = 0
                            print(f"[DEBUG] Speech detected! Recording started at {datetime.now().strftime('%H:%M:%S')}")
                            recorder.buffer_frame(frame)
                            consecutive_voiced = 0
                    else:
                        consecutive_voiced = 0

                elif state == STATE_RECORDING:
                    recorder.buffer_frame(frame)
                    if is_speech:
                        consecutive_silence = 0
                    else:
                        consecutive_silence += 1
                        if consecutive_silence >= silence_frames:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = os.path.join(OUTPUT_DIR, f"recording_{timestamp}.wav")
                            recorder.save_recording(filename)
                            state = STATE_IDLE
                            consecutive_silence = 0
                            consecutive_voiced = 0
                            print("[DEBUG] Waiting for next speech segment...")

        except KeyboardInterrupt:
            print("\nDEBUG: Exiting...")
        finally:
            recorder.stop_stream()
            print(f"DEBUG: Log saved to {log_file}")

if __name__ == "__main__":
    main()
