import ctypes
import tkinter as tk


class Overlay:
    def __init__(self, root):
        self.root = root
        self.label = tk.Label(root, text="New Overlay", bg="green")
        self.label.pack()

        self.setup_ui()

        self.root.after(100, lambda: self.position_label())
        self.root.after(100, lambda: self.allow_clickthrough())

    def setup_ui(self):
        self.root.title("overlay")
        self.root.attributes("-topmost", True)
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-transparentcolor", "red")
        self.root.configure(bg="red")
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
        self.label.config(text=text)

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
