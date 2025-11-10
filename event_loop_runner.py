# async_loop_runner.py
import asyncio
import json

loop = asyncio.new_event_loop()

def start_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

def run_async(coro):
    """Schedule a coroutine in the global event loop"""
    return asyncio.run_coroutine_threadsafe(coro, loop)

# global variable to hold a reference to the websocket client
client_ref = None

def register_client(ws):
    """Called from websockets.main when a client connects"""
    global client_ref
    client_ref = ws

async def send_event(event_type, data=None):
    global client_ref
    if client_ref is None:
        print("No client connected, cannot send event")
        return

    message = json.dumps({"type": event_type, "data": data or {}})
    try:
        await client_ref.send_text(message)
    except Exception as e:
        print("Failed to send event:", e)
        client_ref = None  # clear if disconnected
