# Description
This folder is only for debugging and testing, nothing here is used in the main program

# Content
- audio_files/ - This folder is for wav files I have downloaded or made myself used for testing
- debug_logs/ - Here i put some csv files I generated for testing(from main_with_debug.py)
- recording_chunks/ - This folder is where chunks are saved when you run test_vad_stream.py(will be created when you run the code)
- audio_convert.ps1 - This file is a powershell script for converting the audio files to the right encoding
- audio_tests.json - This file is a json file I wrote manually for keeping track of the audio file tests
- test_vad_stream.py - This file has code for testing VAD on wav files
- main_with_debug.py - This file is the same as main.py but with lots of debug output(would have to be in the root with recording.py to work)