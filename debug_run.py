"""
Easy debug launcher

Usage:
    python debug_run.py
"""
import test_debug.voice_detection.recorded_test as recorded_test
import test_debug.voice_detection.live_test as live_test
import test_debug.transcribe.main_test as transcribe_test 


def main():
    print("Select debug script to run:")
    print("1) Voice detection recorded test")
    print("2) Voice detection live test")
    print("3) Transcribe test")
    choice = input("Enter 1, 2, or 3: ").strip()

    if choice == "1":
        filename = input("Enter audio filename(in audio_files folder) ").strip()
        recorded_test.main(filename)

    elif choice == "2":
        live_test.main()

    elif choice == "3":
        filename = input("Enter audio filename(in audio_files folder) ").strip()
        transcribe_test.transcribe_audio(filename)

    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
