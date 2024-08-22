import base64
import hashlib
import json
import logging
import threading

from websocket import WebSocketApp

from src.events import IEventManager

logger = logging.getLogger(__name__)


class WebSocketClient:
    def __init__(
        self, event_manager: IEventManager, url: str, port: str, password: str
    ):
        self._event_manager = event_manager
        self._ws: WebSocketApp = None
        self._stop_event = threading.Event()
        self._retry_event = threading.Event()

        self._url = url
        self._port = port
        self._password = password

    def run(self) -> None:
        while not self._stop_event.is_set():
            if self._retry_event.is_set():
                self._retry_event.clear()
                self.__connect()
            else:
                self.__connect()
                self._ws.close()
                self._retry_event.wait(timeout=5)

    def set_credentials(self, url: str, port: str, password: str) -> None:
        self._url = url
        self._port = port
        self._password = password
        self.__retry_connection()

    def __connect(self):
        self._ws = WebSocketApp(
            f"ws://{self._url}:{self._port}",
            on_message=self.__on_message,
            on_close=self.__on_close,
        )
        self._ws.run_forever()

    def __on_close(self, ws, close_status_code, close_msg):
        logger.info(
            f'Connection lost. Is OBS running? | Code "{close_status_code}" | Message "{close_msg}"'
        )
        self._event_manager.notify("connection", {"isConnected": False})

    def __retry_connection(self):
        if self._ws:
            self._ws.close()
        self._retry_event.set()
        logger.info("Connection configuration updated, attempting to connect...")

    def __on_message(self, ws: WebSocketApp, message: str):
        data = json.loads(message)
        if "op" in data:
            if data["op"] == 0:
                self.__handle_identify_message(ws, data)
            elif data["op"] == 2:
                self.__handle_identify_response_message(ws, data)
            elif data["op"] == 5 or data["d"]["requestId"] == "getRecordStatus":
                self.__handle_recording_status_response_message(ws, data)

    def __handle_identify_message(self, ws: WebSocketApp, data):
        identify_payload = {}
        if "authentication" in data["d"]:
            salt = data["d"]["authentication"]["salt"]
            challenge = data["d"]["authentication"]["challenge"]
            auth_response = self.__generate_auth_response(salt, challenge)
            identify_payload = {
                "op": 1,
                "d": {"rpcVersion": 1, "authentication": auth_response},
            }
        ws.send(json.dumps(identify_payload))

    def __handle_identify_response_message(self, ws: WebSocketApp, data):
        isConnected = False
        if data["d"]["negotiatedRpcVersion"] == 1:
            logger.info("Authenticated successfully")
            isConnected = True
            self.__request_recording_status(ws)
        else:
            logger.info(
                "Failed to authenticate - is your OBS websocket password correct?"
            )

        self._event_manager.notify("connection", {"isConnected": isConnected})

    def __generate_auth_response(self, salt, challenge):
        password_salt = self._password + salt

        sha256_hash = hashlib.sha256(password_salt.encode()).digest()
        base64_secret = base64.b64encode(sha256_hash).decode()

        secret_challenge = base64_secret + challenge

        final_hash = hashlib.sha256(secret_challenge.encode()).digest()
        auth_response = base64.b64encode(final_hash).decode()

        return auth_response

    def __request_recording_status(self, ws: WebSocketApp):
        if ws and ws.sock and ws.sock.connected:
            recording_status_payload = {
                "op": 6,
                "d": {"requestType": "GetRecordStatus", "requestId": "getRecordStatus"},
            }

            ws.send(json.dumps(recording_status_payload))

    def __handle_recording_status_response_message(self, ws: WebSocketApp, data):
        recording_status = "stopped"

        if data["op"] == 5:
            state = data["d"]["eventData"]["outputState"]
            if "OUTPUT_START" in state or "OUTPUT_RESUMED" in state:
                recording_status = "recording"
            elif "OUTPUT_PAUSED" in state:
                recording_status = "paused"
        else:
            state = data["d"]["responseData"]
            if state["outputPaused"]:
                recording_status = "paused"
            elif state["outputActive"]:
                recording_status = "recording"

        self._event_manager.notify("status", {"status": recording_status})
