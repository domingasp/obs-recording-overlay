import ctypes
import tkinter as tk
from PIL import Image, ImageTk

def load_image(path):
    image = Image.open(path)
    image.resize((20, 20), Image.LANCZOS)
    return ImageTk.PhotoImage(image)


class Overlay:
    def __init__(self, root):
        self.load_overlay_images()

        self.root = root
        self.label = tk.Label(root, image=self.images['pausedImage'], bg='blue', borderwidth=0, highlightthickness=0)

        self.setup_ui()

        self.root.after(100, lambda: self.allow_clickthrough())

    def load_overlay_images(self):
        self.images = {
            'pausedImage': load_image('assets/paused-icon.png')
        }

    def setup_ui(self):
        self.root.title("overlay")
        self.root.attributes("-topmost", True)
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-transparentcolor", "blue")
        self.root.configure(bg="blue")
        self.root.overrideredirect(True)

    def position_label(self):
        """Moves label to bottom right of screen."""
        self.label.update_idletasks()
        label_width = self.label.winfo_width()
        label_height = self.label.winfo_height()

        x_pos = self.root.winfo_screenwidth() - label_width
        y_pos = self.root.winfo_screenheight() - label_height

        self.label.place(x=x_pos, y=y_pos)

    def update_label(self, text):
        self.label.config(image=self.images['pausedImage'])
        if text == 'stopped':
            self.label.place_forget()
        else:
            self.position_label()

    def allow_clickthrough(self):
        """Adds windows flags to `hwnd` allowing clickthrough.

        WS_EX_LAYERED, WS_EX_TRANSPARENT, SWP_NOMOVE, SWP_NOSIZE
        SWP_NOACTIVATE, SWP_TOPMOST
        """
        user32 = ctypes.windll.user32
        hwnd = user32.FindWindowW(None, "overlay")
        if hwnd:
            styles = user32.GetWindowLongW(hwnd, -20)

            # Add WS_EX_LAYERED | WS_EX_TRANSPARENT
            user32.SetWindowLongW(hwnd, -20, styles | 0x80000 | 0x20)

            # Add SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE | SWP_TOPMOST
            user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0010 | 0x0001 | 0x0004 | 0x0008)
