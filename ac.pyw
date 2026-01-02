#    ____  __           ____ _       ____________  ________  ______ _____ _____ __ __
#   / __ \/ /__  ____ _/ __ \ |     / / ____/ __ \/_  __/\ \/ ( __ )__  // ___// // /
#  / / / / / _ \/ __ `/ / / / | /| / / __/ / /_/ / / /    \  / __  |/_ </ __ \/ // /_
# / /_/ / /  __/ /_/ / /_/ /| |/ |/ / /___/ _, _/ / /     / / /_/ /__/ / /_/ /__  __/
# \____/_/\___/\__, /\___\_\|__/|__/_____/_/ |_| /_/     /_/\____/____/\____/  /_/
#             /____/

import tkinter as tk
from tkinter import ttk
import threading
import time
import keyboard
from pynput.mouse import Button, Controller


class AC:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry("170x110")
        self.root.resizable(False, False)

        self.mouse = Controller()
        self.running = False
        self.interval = 0.1
        self.setup_ui()
        keyboard.add_hotkey('alt+x', self.toggle_clicker)

    def setup_ui(self):
        self.slider = ttk.Scale(self.root, from_=1, to=100, command=self.update_interval)
        self.slider.set(10)
        self.slider.pack(pady=10, padx=20, fill='x')

        self.mouse_var = tk.StringVar(value="left")

        for text, value in [("ЛКМ", "left"), ("ПКМ", "right")]:
            frame = tk.Frame(self.root)
            tk.Radiobutton(frame, variable=self.mouse_var, value=value).pack(side='left')
            tk.Label(frame, text=text).pack(side='left', padx=2)
            frame.pack(pady=2)

    def update_interval(self, val):
        cps = float(val)
        self.interval = 1.0 / cps if cps > 0 else 0

    def click_loop(self):
        button = Button.left if self.mouse_var.get() == "left" else Button.right
        while self.running:
            self.mouse.click(button)
            time.sleep(self.interval)

    def toggle_clicker(self):
        self.running = not self.running
        if self.running:
            threading.Thread(target=self.click_loop, daemon=True).start()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    AC().run()