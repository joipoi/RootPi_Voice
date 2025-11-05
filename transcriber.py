import whisper
import time

LANGUAGE = "sv" # swedish = sv, english = en
MODEL = "small" # tiny/base/small/medium/large/turbo

def transcribe_audio(filename="test.wav"):
    print("🧠 Loading Whisper model...")
    model = whisper.load_model(MODEL) 

    print(f"🎧 Transcribing '{filename}'...")
    start_time = time.time()  # Start timer

    result = model.transcribe(filename, language=LANGUAGE)

    end_time = time.time()  # End timer
    elapsed = end_time - start_time

    print("\n📝 Transcription:")
    print(result["text"])

    print(f"\n⏱️ Transcription time: {elapsed:.2f} seconds")
    return result["text"]

if __name__ == "__main__":
    transcribe_audio()
