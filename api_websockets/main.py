# websockets/main.py
from fastapi import FastAPI, WebSocket
import threading

from voice_main import start_recording_loop
from event_loop_runner import register_client

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    register_client(ws)  # tell the loop module about this client
    print("Client connected")

    try:
        while True:
            # Optional: receive messages (not required for your use case)
            data = await ws.receive_text()
            print("Received:", data)
            if data == "start_recording":
                threading.Thread(target=start_recording_loop, daemon=True).start()
            
    except Exception:
        print("Client disconnected")
    finally:
        register_client(None)


