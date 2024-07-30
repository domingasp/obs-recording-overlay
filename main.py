import logging
import threading
import tkinter as tk

from WebSocketClient import WebSocketClient
from logging_config import setup_logging
from Overlay import Overlay

setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    root = tk.Tk()
    overlay = Overlay(root)

    ws_client = WebSocketClient(overlay)
    threading.Thread(target=ws_client.run, daemon=True).start()

    root.mainloop()