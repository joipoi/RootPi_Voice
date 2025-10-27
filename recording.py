# recording.py
import sounddevice as sd
import numpy as np
import queue
import threading
import time
import wave
from collections import deque

class Frame:
    """Represents a single audio frame."""
    def __init__(self, bytes_data, timestamp, duration):
        self.bytes = bytes_data
        self.timestamp = timestamp
        self.duration = duration

class Recorder:
    def __init__(self, sample_rate=16000, frame_duration_ms=30):
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_size = int(sample_rate * frame_duration_ms / 1000)  # samples per frame
        self.audio_queue = queue.Queue()
        self.recording_buffer = []
        self.stream = None
        self.running = False
        self.start_time = None

    def _callback(self, indata, frames, time_info, status):
        """This callback runs in a separate thread and puts audio into the queue."""
        if status:
            print(f"Sounddevice status: {status}", flush=True)
        # Convert to 16-bit PCM bytes
        pcm_data = (indata[:, 0] * 32767).astype(np.int16).tobytes()
        timestamp = time.time() - self.start_time
        frame = Frame(pcm_data, timestamp, self.frame_duration_ms / 1000.0)
        self.audio_queue.put(frame)

    def start_stream(self):
        """Start microphone stream in a separate thread."""
        self.running = True
        self.start_time = time.time()
        self.stream = sd.InputStream(
            channels=1,
            samplerate=self.sample_rate,
            dtype='float32',
            blocksize=self.frame_size,
            callback=self._callback
        )
        self.stream.start()

    def stop_stream(self):
        """Stop microphone stream."""
        self.running = False
        if self.stream:
            self.stream.stop()
            self.stream.close()

    def frames(self):
        """Generator that yields frames from the queue."""
        while self.running:
            try:
                frame = self.audio_queue.get(timeout=0.1)
                yield frame
            except queue.Empty:
                continue

    def start_recording(self):
        """Start buffering frames for saving later."""
        self.recording_buffer = []

    def buffer_frame(self, frame):
        """Add a frame to the recording buffer."""
        self.recording_buffer.append(frame)

    def save_recording(self, filename):
        """Write buffered frames to a WAV file."""
        if not self.recording_buffer:
            print("No frames to save.")
            return
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit PCM
            wf.setframerate(self.sample_rate)
            # Combine all frames
            audio_bytes = b''.join(f.bytes for f in self.recording_buffer)
            wf.writeframes(audio_bytes)
        print(f"Saved recording: {filename}")
        self.recording_buffer = []
