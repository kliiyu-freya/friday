# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "websocket-client",
# ]
# ///
from websocket import create_connection
import time
import json

import src.assistant as assistant

WS_URL = "ws://host.docker.internal:6672/ws"
WS_TYPE_IN = "friday_assistant_request"
WS_TYPE_OUT = "friday_assistant_response"


def connect_to_server():
    """Connect to the WebSocket server with retry logic."""
    while True:
        try:
            ws = create_connection(WS_URL)
            print(f"Connected to WebSocket server at {WS_URL}")
            return ws
        except Exception as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)


def on_message(ws) -> str:
    """Receive a message from the WebSocket server."""
    while True:
        try:
            result = ws.recv()
            data = json.loads(result)

            if data.get("type") == WS_TYPE_IN:
                print(f"Received message: {data}")
                return data["data"]["content"]
            
        except Exception as e:
            print(f"Error receiving message: {e}")


def respond(ws, content: dict):
    """Send a response to the WebSocket server."""
    try:
        signed_data = {
            "type": WS_TYPE_OUT,
            "data": {
                "content": content
            }
        }
        message = json.dumps(signed_data)
        ws.send(message)
        print(f"Sent: {message}")
            
    except Exception as e:
        print(f"Error: {e}")


def main():
    ws = connect_to_server()
    friday = assistant.new(verbose=True, testing=True)

    while True:
        message = on_message(ws)
        content = friday.prompt(message)
        respond(ws, content)


if __name__ == "__main__":
    print("Starting Friday Assistant...")
    main()
