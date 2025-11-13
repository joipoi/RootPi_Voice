
# Adjusting Algorhytm
To get the Voice activity detection to work better there are some variables you can adjust. Some of them can only have fixed values decided by webrtcvad and others are made by me

Feel free to change these and test if it gets better or worse
```python
SAMPLE_RATE = 16000 # can only be 8000/16000/32000/48000
FRAME_DURATION_MS = 30 # can only be 10/20/30
VAD_AGGRESSIVENESS = 3  # can only be 0/1/2/3
SILENCE_DURATION_MS = 1000 # how many ms of silence until we stop recording
PREBUFFER_DURATION_MS = 500  # store last milliseconds of audio before speech
VALIDATION_FRAMES = 15 # require this many consecutive voiced frames to start recording
# The amount of ms as voice needed to trigger recording =  VALIDATION_FRAMES * FRAME_DURATION_MS, currently 15*30=450ms
```

# Problems
Currently the program is good at telling the difference between silence and sound. It is also good at knowing when the sound stops and to stop the recording. However it can not tell the difference between voice and for example keyboard clicking. We can get it to ignore some background sound but if it is loud enough it will start the recording which seems bad. 

# Debug
For debugging run

```
python debug_run.py
```

# Audio file conversion
(This is only relevent for debugging, not for our main program)

When creating or downloading wav files they might not be encoded right. We can fix this by using [ffmpeg](https://www.ffmpeg.org/). I already had ffmpeg installed by maybe you need to install it.

To encode one file with ffmpeg you can use this command
```
ffmpeg -i file.wav -ar 16000 -ac 1 -f wav encoded_file.wav
```
I have made a powershell script that encodes all the audio files in the "audio_files" directory. Simply open powershell in the test_debug folder and type "./audio_convert.ps1"

# Threads
Because we are constantly recording and also querying ai and sending websockets event, we have to use threads and do async stuff.

I am not great at python threads so that code might have problems. I made a file to handle this called "event_loop_runner.py"