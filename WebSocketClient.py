import base64
import hashlib
import json
import logging
import time
import websocket

logger = logging.getLogger(__name__)


class WebSocketClient:
    def __init__(self, overlay):
        self.overlay = overlay
        self.ws = None

    def run(self):
        ws = websocket.WebSocketApp(
            "ws://localhost:4455", on_message=self.on_message, on_close=self.on_close
        )

        while True:
            ws.run_forever()
            time.sleep(5)
            logger.info("Attempting to reconnect...")

    def on_open(self, ws):
        auth_payload = {"request-type": "GetAuthRequired", "message-id": "auth"}
        ws.send(json.dumps(auth_payload))

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(
            f'Connection lost. Is OBS running? | Code "{close_status_code}" | Message "{close_msg}"'
        )

    def on_message(self, ws, message):
        """Websocket message handler.

        For details on OBS Opcodes - https://github.com/obsproject/obs-websocket/blob/master/docs/generated/protocol.md#websocketclosecodemessagedecodeerror
        """
        data = json.loads(message)
        if "op" in data:
            if data["op"] == 0:
                if "authentication" in data["d"]:
                    salt = data["d"]["authentication"]["salt"]
                    challenge = data["d"]["authentication"]["challenge"]
                    auth_response = self.generate_auth_response(
                        salt=salt, challenge=challenge
                    )
                    identify_payload = {
                        "op": 1,
                        "d": {"rpcVersion": 1, "authentication": auth_response},
                    }
                ws.send(json.dumps(identify_payload))
            elif data["op"] == 2:
                if data["d"]["negotiatedRpcVersion"] == 1:
                    logger.info("Authenticated successfully")
                else:
                    logger.info(
                        "Failed to authenticate - is your OBS websocket password correct?"
                    )
            elif data["op"] == 5:
                state = data["d"]["eventData"]["outputState"]
                obs_recording_state = "stopped"
                if "OUTPUT_STARTED" in state or "OUTPUT_RESUMED" in state:
                    obs_recording_state = "recording"
                elif "OUTPUT_PAUSED" in state:
                    obs_recording_state = "paused"

                self.overlay.update_label(obs_recording_state)

    def generate_auth_response(self, salt, challenge):
        obs_password = ""
        with open("obs_password.txt") as file:
            obs_password = file.read()

        password_salt = obs_password + salt

        sha256_hash = hashlib.sha256(password_salt.encode()).digest()
        base64_secret = base64.b64encode(sha256_hash).decode()

        secret_challenge = base64_secret + challenge

        final_hash = hashlib.sha256(secret_challenge.encode()).digest()
        auth_response = base64.b64encode(final_hash).decode()
        return auth_response
