import tkinter as tk
from tkinter import ttk
import json  # Importing the json module to handle JSON data
import json_manager
import audio_manager
import os
from board_tab import BoardTab
from setup_tab import SetupTab
from sound_importer import SoundImporter
import oofKey

# Load keylist and data
keylist = {}

json_manager.check_startup()

data = json_manager.load_data()

# Create the main window
root = tk.Tk()
root.title("Echo")
root.iconbitmap(json_manager.icon_file, default=json_manager.icon_file)
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

sound_importer = SoundImporter(notebook, data, data["settings"])
notebook.add(sound_importer, text="Import Sounds")

OutOfFocusHandler = oofKey.OOFKeyHandler(setup_tab, board_tab)

# Pack the notebook
notebook.pack(expand=True, fill="both")

def on_focus_in(event):
    OutOfFocusHandler.simulating = False

def on_focus_out(event):
    OutOfFocusHandler.simulating= True

root.bind("<FocusIn>", on_focus_in)
root.bind("<FocusOut>", on_focus_out)

# Start the main loop
root.mainloop()
