import base64
import hashlib
import json
import logging
import threading
import time
import websocket

logger = logging.getLogger(__name__)


class WebSocketClient:
    def __init__(self, overlay):
        self.overlay = overlay
        self.ws = None

        self.websocket_url = "localhost"
        self.websocket_port = "4455"
        self.websocket_password = ""

        self._stop_event = threading.Event()
        self._retry_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            if self._retry_event.is_set():
                self._retry_event.clear()
                self.connect()
            else:
                self.connect()
                self.ws.close()
                self._retry_event.wait(timeout=5)

    def connect(self):
        self.ws = websocket.WebSocketApp(
            f"ws://{self.websocket_url}:{self.websocket_port}",
            on_message=self.on_message,
            on_close=self.on_close,
        )
        self.ws.run_forever()

    def on_open(self, ws):
        auth_payload = {"request-type": "GetAuthRequired", "message-id": "auth"}
        ws.send(json.dumps(auth_payload))

    def on_close(self, ws, close_status_code, close_msg):
        logger.info(
            f'Connection lost. Is OBS running? | Code "{close_status_code}" | Message "{close_msg}"'
        )
        self.overlay.update_connected(False)

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
                    self.overlay.update_connected(True)
                    self.request_recording_status()
                else:
                    logger.info(
                        "Failed to authenticate - is your OBS websocket password correct?"
                    )
                    self.overlay.update_connected(False)
            elif data["op"] == 5 or data["d"]["requestId"] == "getRecordStatus":
                obs_recording_state = "stopped"

                if data["op"] == 5:
                    state = data["d"]["eventData"]["outputState"]
                    if "OUTPUT_START" in state or "OUTPUT_RESUMED" in state:
                        obs_recording_state = "recording"
                    elif "OUTPUT_PAUSED" in state:
                        obs_recording_state = "paused"
                else:
                    state = data["d"]["responseData"]
                    if state["outputPaused"]:
                        obs_recording_state = "paused"
                    elif state["outputActive"]:
                        obs_recording_state = "recording"

                self.overlay.update_label(obs_recording_state)

    def generate_auth_response(self, salt, challenge):
        password_salt = self.websocket_password + salt

        sha256_hash = hashlib.sha256(password_salt.encode()).digest()
        base64_secret = base64.b64encode(sha256_hash).decode()

        secret_challenge = base64_secret + challenge

        final_hash = hashlib.sha256(secret_challenge.encode()).digest()
        auth_response = base64.b64encode(final_hash).decode()
        return auth_response

    def set_websocket_url(self, url):
        self.websocket_url = url

    def set_websocket_port(self, port):
        self.websocket_port = port

    def set_websocket_password(self, password):
        self.websocket_password = password

    def retry_connection(self):
        if self.ws:
            self.ws.close()
        self._retry_event.set()
        logger.info("Connection configuration updated, attempting to connect...")

    def request_recording_status(self):
        if self.ws and self.ws.sock and self.ws.sock.connected:
            request_payload = {
                "op": 6,
                "d": {
                    "requestType": "GetRecordStatus",
                    "requestId": "getRecordStatus",
                },
            }
            self.ws.send(json.dumps(request_payload))
