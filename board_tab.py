import tkinter as tk
from tkinter import ttk
import audio_manager

class BoardTab(ttk.Frame):
    def __init__(self, parent, button_data_list):
        super().__init__(parent)
        self.button_data_list = button_data_list  # List of button data entries
        self.create_widgets()
        self.bind('<KeyPress>', self.handle_keypress)

    def create_widgets(self):
        self.buttons = []  # Store button references to access them later

        # Loop through button_data_list to create multiple buttons
        for button_data in self.button_data_list:
            # Create a button for each entry
            button = ttk.Button(self, text=button_data["name"], command=lambda bd=button_data: self.play_audio(bd))
            button.pack(anchor="nw", padx=10, pady=10)  # Align buttons to the top-left
            self.buttons.append((button, button_data))  # Keep track of button and its data

    def play_audio(self, button_data):
        # Play audio specific to the button
        if "sound_path" in button_data and button_data["sound_path"]:
            audio_manager.play_audio(button_data["sound_path"], button_data["volume"])

    def handle_keypress(self, event):
        pressed_key = event.keysym.upper()  # Convert the pressed key to uppercase
        # print(f"Keypressed: {pressed_key}")
        # Iterate over all buttons to check their keybinds
        for button, button_data in self.buttons:
            #print(" Checking " + button_data["name"])
            keybind = button_data.get("keybind", "").upper()  # Keybind for each button
            #print(f"    Keybind: {keybind}")
            if pressed_key == keybind and keybind:  # Match the pressed key with the button's keybind
                button.invoke()  # Simulate a button press
                return "break"
    
