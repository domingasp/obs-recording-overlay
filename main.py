import base64
import hashlib
import hmac
import threading
import websocket
import json

obs_password = ""
with open("obs_password.txt") as file:
    obs_password = file.read()


def generate_auth_response(salt, challenge):
    password_salt = obs_password + salt

    sha256_hash = hashlib.sha256(password_salt.encode()).digest()
    base64_secret = base64.b64encode(sha256_hash).decode()

    secret_challenge = base64_secret + challenge

    final_hash = hashlib.sha256(secret_challenge.encode()).digest()
    auth_response = base64.b64encode(final_hash).decode()
    return auth_response


def on_message(ws, message):
    data = json.loads(message)
    if "op" in data:
        if data["op"] == 0:
            if "authentication" in data["d"]:
                salt = data["d"]["authentication"]["salt"]
                challenge = data["d"]["authentication"]["challenge"]
                auth_response = generate_auth_response(salt=salt, challenge=challenge)
                identify_payload = {
                    "op": 1,
                    "d": {"rpcVersion": 1, "authentication": auth_response},
                }
            ws.send(json.dumps(identify_payload))
        elif data["op"] == 2:
            if data["d"]["negotiatedRpcVersion"] == 1:
                print("Authenticated successfully")


def on_open(ws):
    auth_payload = {"request-type": "GetAuthRequired", "message-id": "auth"}
    ws.send(json.dumps(auth_payload))


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "ws://localhost:4455",
        on_message=on_message,
    )

    ws.run_forever()
