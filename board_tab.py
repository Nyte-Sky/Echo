import tkinter as tk
from tkinter import ttk
import audio_manager

class BoardTab(ttk.Frame):
    def __init__(self, parent, button_data):
        super().__init__(parent)
        self.button_data = button_data
        self.create_widgets()
        self.bind('<KeyPress>', self.handle_keypress)  # Bind keypress events

    def create_widgets(self):
        # Align the button to the top left
        self.button = ttk.Button(self, text=self.button_data["name"], command=self.play_audio)
        self.button.pack(anchor="nw", padx=10, pady=10)  # Use anchor for top-left alignment

    def play_audio(self):
        if "sound_path" in self.button_data and self.button_data["sound_path"]:
            audio_manager.play_audio(self.button_data["sound_path"], self.button_data["volume"])

    def handle_keypress(self, event):
        keybind = self.button_data.get("keybind", "").upper()  # Keybind is stored as uppercase
        pressed_key = event.keysym.upper()  # Convert the pressed key to uppercase
        # print(f"Pressed key: {pressed_key}, Expected keybind: {keybind}")
        
        if pressed_key == keybind and keybind:  # Match the keysym with the keybind
            self.button.invoke()  # Simulate a button press
            # print(f"Triggered button for keybind: {keybind}")  # Confirm trigger


