# Alternative to transcriber.py that uses api instead of running locally

from openai import OpenAI
import time

LANGUAGE = "sv" # swedish = sv, english = en
MODEL = "whisper-1" # tiny/base/small/medium/large/turbo

def transcribe_audio_api(filename="test.wav"):
    start_time = time.time()  # Start timer
    client = OpenAI()

    print(f"🎧 Transcribing '{filename}'...")
    with open(filename, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=MODEL,
            file=audio_file,
            language=LANGUAGE
        )

    end_time = time.time()  # End timer
    elapsed = end_time - start_time

    print("\n📝 Transcription:")
    print(transcription.text)

    print(f"\n⏱️ Transcription time: {elapsed:.2f} seconds")
    return transcription.text

if __name__ == "__main__":
    transcribe_audio_api()
