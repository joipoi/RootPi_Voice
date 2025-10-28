# main.py
import os
import time
from datetime import datetime
import webrtcvad
from collections import deque

from recording import Recorder, Frame

# --- PARAMETERS ---
SAMPLE_RATE = 16000 # can only be 8000/16000/32000/48000
FRAME_DURATION_MS = 30 # can only be 10/20/30
VAD_AGGRESSIVENESS = 3  # can only be 0/1/2/3
SILENCE_DURATION_MS = 1000 # how many ms of silence until we stop recording
PREBUFFER_DURATION_MS = 500  # store last milliseconds of audio before speech
VALIDATION_FRAMES = 15 # require this many consecutive voiced frames to start recording
# The amount of ms as voice needed to trigger recording =  VALIDATION_FRAMES * FRAME_DURATION_MS, currently 15*30=450ms

OUTPUT_DIR = "recordings"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)
    recorder = Recorder(sample_rate=SAMPLE_RATE, frame_duration_ms=FRAME_DURATION_MS)
    recorder.start_stream()
    print("Listening for speech... Press Ctrl+C to stop.")

    STATE_IDLE = 0
    STATE_RECORDING = 1
    state = STATE_IDLE

    silence_frames = int(SILENCE_DURATION_MS / FRAME_DURATION_MS)
    prebuffer_frames = int(PREBUFFER_DURATION_MS / FRAME_DURATION_MS)

    consecutive_silence = 0
    consecutive_voiced = 0
    prebuffer = deque(maxlen=prebuffer_frames)

    try:
        for frame in recorder.frames():
            is_speech = vad.is_speech(frame.bytes, SAMPLE_RATE)
            prebuffer.append(frame)

            if state == STATE_IDLE:
                if is_speech:
                    consecutive_voiced += 1
                    if consecutive_voiced >= VALIDATION_FRAMES:
                        # Start recording
                        state = STATE_RECORDING
                        recorder.start_recording()
                        # Add prebuffer to recording
                        for f in prebuffer:
                            recorder.buffer_frame(f)
                        prebuffer.clear()
                        consecutive_silence = 0
                        print(f"Speech detected! Recording started at {datetime.now().strftime('%H:%M:%S')}")
                        recorder.buffer_frame(frame)  # current frame
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
                        # Stop recording
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = os.path.join(OUTPUT_DIR, f"recording_{timestamp}.wav")
                        recorder.save_recording(filename)
                        state = STATE_IDLE
                        consecutive_silence = 0
                        consecutive_voiced = 0
                        print("Waiting for next speech segment...")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        recorder.stop_stream()

if __name__ == "__main__":
    main()
