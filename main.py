import base64
import hashlib
import hmac
import logging
import threading
import time
import websocket
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

def update_obs_recording_state_file(state):
    with open('obs_recording_state.txt', 'w+') as file:
        file.write(state)

def on_message(ws, message):
    """Websocket message handler.
    
    For details on OBS Opcodes - https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#websocketclosecodemessagedecodeerror
    """
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
                logger.info("Authenticated successfully")
            else:
                logger.info("Failed to authenticate - is your OBS websocket password correct?")
        elif data['op'] == 5:
            state = data['d']['eventData']['outputState']
            obs_recording_state = 'stopped'
            if 'OUTPUT_STARTED' in state or 'OUTPUT_RESUMED' in state:
                obs_recording_state = 'recording'
            elif 'OUTPUT_PAUSED' in state:
                obs_recording_state = 'paused'

            update_obs_recording_state_file(obs_recording_state)

def on_open(ws):
    auth_payload = {"request-type": "GetAuthRequired", "message-id": "auth"}
    ws.send(json.dumps(auth_payload))


def on_close(ws, close_status_code, close_msg):
    logger.info(
        f'Connection lost. Is OBS running? | Code "{close_status_code}" | Message "{close_msg}"'
    )


if __name__ == "__main__":
    websocket.enableTrace(True)
    while True:
        ws = websocket.WebSocketApp(
            "ws://localhost:4455", on_message=on_message, on_close=on_close
        )
        ws.run_forever()

        time.sleep(5)
        logger.info("Attempting to reconnect...")
