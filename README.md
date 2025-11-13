# Description
The flow of the program goes like this(not counting api):

- The program starts listening for audio(using sounddevice)
- When it recognizes a voice it starts recording and when the voice stops it stops recording.(using [webrtcvad](https://github.com/wiseman/py-webrtcvad))
- Each recording is saved as a wav file. 
- The wav fle is converted to text with OpenAI Whisper.
- The text is sent to an AI(openai) that uses tool/function calling to run some code based on the text

The main program can be run from voice_main.py, however there is also an api with websockets that you can run via init.py, in that case the recording starts when a websocket event is recieved

# Setup
Setup a python envrioment and install dependencies from requirements.txt with these commands

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
When I installed webrtcvad I got some error about Visual Studio and C++. To solve this I had to go to this [link](https://visualstudio.microsoft.com/visual-cpp-build-tools/) and download the "Visual Studio Build Tools for C++". Then I had to go to Visual Studio installer and install "Desktop development with C++". Then I could install webrtcvad with no problem.

You also need a .env file where you insert an OpenAI key, this is needed for tool calling and transcription if you are not running it locally

# Usage
To run with the api and websockets:
```
python init.py
```
Then the recording starts when we get an event from the frontend and we send events to the frontend based on what the user said


to run without api just the main recording loop(does not work right now)
```
python voice_main.py
```
then start speaking into your microphone and you will see wav files in the "recordings" folder and see transcriptions in the console
# Transcribing
For the transcribing we are using openai whisper. 

There is an option for running locally(transcriber.py) and one for running via API(transcriber_api.py)

You can set it to local or api with the variable "TRANSCRIBE_METHOD" in voice_main.py

# Tool Calling
To know what function to call based on text we use tool calling or as OpenAI calls it [function calling](https://platform.openai.com/docs/guides/function-calling).

The code for this is in the tool_calling folder. We define our tools in the file called "ai_tools.py" and then we query the ai with all the tools attached.

# Websockets
We want something to happen in a different application based on what the user said. So we need to send events from this program to another one. We used [Websockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) for this.

The tools we gave to the ai are the ones that send events to our other application. Here is an example of the event data we send:
```
("runFunction", {"name": "write_question", "args": question})
```

We also can start our recording based on an event we recieve from the other application. like this:
```
 data = await ws.receive_text()
    if data == "start_recording":
        threading.Thread(target=start_recording_loop, daemon=True).start()
```
