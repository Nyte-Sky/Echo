import tkinter as tk
from tkinter import ttk
import json  # Importing the json module to handle JSON data
import json_manager
import audio_manager
import os
from board_tab import BoardTab
from setup_tab import SetupTab

# FInd if self.image_label exists in setup.py line 94 so we can show/hid bg image on toggle.

# Load keylist from JSON file
def load_keylist():
    keylist_file = "keylist.json"
    if os.path.exists(keylist_file):
        with open(keylist_file, 'r') as f:
            return json.load(f)
    else:
        return {}

# Load keylist and data
keylist = load_keylist()
data = json_manager.load_data()

# Create the main window
root = tk.Tk()
root.title("Echo")
root.geometry("650x600")

# Initialize audio
audio_manager.initialize_audio()

# Create a Notebook (tab container)
notebook = ttk.Notebook(root)

# Create the "Board" tab
board_tab = BoardTab(notebook, data["buttons"], data["settings"])
# Add this line after creating the BoardTab
root.bind('<KeyPress>', lambda event: board_tab.handle_keypress(event))
notebook.add(board_tab, text="Board")

# Create the "Setup" tab
setup_tab = SetupTab(notebook, data["buttons"], data["settings"], data, keylist, board_tab)  # Pass keylist here
notebook.add(setup_tab, text="Setup")

# Pack the notebook
notebook.pack(expand=True, fill="both")

# Start the main loop
root.mainloop()
