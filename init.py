import threading
import uvicorn
from event_loop_runner import start_loop

def start_loop_thread():
    # Run the async event loop in a daemon thread
    threading.Thread(target=start_loop, daemon=True).start()

if __name__ == "__main__":
    # Start the async event loop
    start_loop_thread()

    print("Starting API server. Press Ctrl+C to stop.")
    # Run Uvicorn in the main thread (not daemon) so it handles Ctrl+C properly
    uvicorn.run("api_websockets.main:app", host="127.0.0.1", port=8000, reload=False)
