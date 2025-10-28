# Description
Currently this project starts listening for audio and when it recognizes a voice it starts recording and when the voice stops it stops recording. It then saves each recording in its own wav file. To recognize the voice it uses [webrtcvad](https://github.com/wiseman/py-webrtcvad). For recording it uses sounddevice
# Setup
Currently I have not tested setting up on another computer so this might be wrong. I should maybe use conda or something similar.

I think the only thing you need is webrtcvad which you get like this
```
pip install webrtcvad
```
When I did this I got some error about Visual Studio and C++. To solve this I had to go to this [link](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and download the "Visual Studio Build Tools for C++". Then I had to go to Visual Studio installer and install "Desktop development with C++". Then I could install webrtcvad with no problem.
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

I want to try some different soultion using another tool, maybe something AI related.

# Audio file conversion
(This is only relevent for debugging, not for our main program)

When creating or downloading wav files they might not be encoded right. We can fix this by using [ffmpeg](https://www.ffmpeg.org/). I already had ffmpeg installed by maybe you need to install it.

To encode one file with ffmpeg you can use this command
```
ffmpeg -i file.wav -ar 16000 -ac 1 -f wav encoded_file.wav
```
I have made a powershell script that encodes all the audio files in the "audio_files" directory. Simply open powershell in the test_debug folder and type "./audio_convert.ps1"
