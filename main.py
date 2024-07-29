import websocket
import json


def on_message(ws, message):
    data = json.loads(message)
    if "update-type" in data:
        if data["update-type"] == "RecordingStarted":
            with open("obs_status.txt", "w") as f:
                f.write("Recording")
        elif data["update-type"] == "RecordingStopped":
            with open("obs_status.txt", "w") as f:
                f.write("Not Recording")


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("### opened ###")
    ws.send(json.dumps({"request-type": "GetStreamingStatus", "message-id": "1"}))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "ws://localhost:4444",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()
