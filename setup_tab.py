import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox, Scale
import json_manager
import audio_manager
import os

class SetupTab(ttk.Frame):
    def __init__(self, parent, button_data, data, keylist):
        super().__init__(parent)
        self.button_data = button_data
        self.data = data
        self.keylist = keylist  # Store keylist for reference
        self.create_widgets()

    def create_widgets(self):
        top_bar = tk.Frame(self, height=20, bg="lightgray")
        top_bar.pack(side="top", fill="x")

        main_area = tk.Frame(self, bg="white", width=500, height=300)
        main_area.pack(expand=True, fill="both")

        bottom_bar = tk.Frame(self, height=20, bg="lightgray")
        bottom_bar.pack(side="bottom", fill="x")

        self.setup_frame = tk.Frame(main_area, bg="lightgray", width=120, height=50, relief="solid", bd=1)
        self.setup_frame.place(x=10, y=10)

        self.update_label()  # Call method to set up the initial label

        self.dropdown_var = tk.StringVar(self.setup_frame)
        self.dropdown_var.set("\u22EF")  # Unicode character for three dots (⋅⋅⋅)

        self.create_dropdown()

    def update_label(self):
        keybind_display = self.button_data.get("keybind", "")
        label_text = self.button_data['name']

        # Clear previous labels if they exist
        if hasattr(self, 'label'):
            self.label.pack_forget()  # Remove the previous label
        if hasattr(self, 'keybind_label'):
            self.keybind_label.pack_forget()  # Remove the previous keybind label

        # Create the button name label
        self.label = tk.Label(self.setup_frame, text=label_text, bg="lightgray")
        self.label.pack(side="left", padx=5)

        if keybind_display:
            # Convert to uppercase if it's a regular letter (A-Z)
            if keybind_display.isalpha() and len(keybind_display) == 1:
                keybind_display = keybind_display.upper()

            # Create the keybind label in blue
            self.keybind_label = tk.Label(self.setup_frame, text=keybind_display, bg="lightgray", fg="blue")
            self.keybind_label.pack(side="left")  # Display keybind in blue

    def create_dropdown(self):
        dropdown_menu = ttk.OptionMenu(self.setup_frame, self.dropdown_var, "\u22EF",
                                         "Change sound", "Rename", "Delete", "Change Keybind", "Change Volume",
                                         command=self.dropdown_action)
        dropdown_menu.pack(side="right", padx=10)

    def dropdown_action(self, action):
        if action == "Change sound":
            self.change_sound()
        elif action == "Rename":
            self.rename_button()
        elif action == "Delete":
            self.delete_button()
        elif action == "Change Keybind":
            self.change_keybind()
        elif action == "Change Volume":
            self.change_volume()

        self.dropdown_var.set("\u22EF")  # Reset to three dots

    def change_volume(self):
         # Create a popup window for volume assignment
        popup = tk.Toplevel(self)
        popup.title("Change Volume")
        popup.geometry("230x125")#
        current_volume = self.button_data.get("volume", "")

        volumeScale = Scale(popup, from_=0, to=10, orient="horizontal")
        volumeScale.set(current_volume * 10)
        volumeScale.pack()

        clear_button = tk.Button(popup, text="Play", command=lambda: audio_manager.play_audio(self.button_data["sound_path"], volumeScale.get()/10))
        clear_button.pack(pady=5)

        # getSize = tk.Button(popup, text="Get size", command=lambda: self.getWinSize(popup))
        # getSize.pack()

        confirm_button = tk.Button(popup, text="Confirm", command=lambda: self.confirm_volume(popup, volumeScale.get()/10))
        confirm_button.pack(side="left", padx=(20, 5), pady=5)

        cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy)
        cancel_button.pack(side="right", padx=(5, 20), pady=5)

    def confirm_volume(self, popup, current_volume):
        self.button_data["volume"] = current_volume
        json_manager.save_data(self.data)  # Save updated data
        popup.destroy()  # Close the popup

    def getWinSize(self, popup):
        print(popup.winfo_height())
        print(popup.winfo_width())

    def change_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")])
        if file_path:
            self.button_data["sound_path"] = file_path
            json_manager.save_data(self.data)
            messagebox.showinfo("Success", "Sound changed successfully!")

    def rename_button(self):
        new_name = simpledialog.askstring("Rename Button", "Enter new name:")
        if new_name:
            self.button_data["name"] = new_name
            self.update_label()  # Update label display
            json_manager.save_data(self.data)

    def delete_button(self):
        result = messagebox.askyesno("Delete Button", "Are you sure you want to delete this button?")
        if result:
            self.data["buttons"].remove(self.button_data)
            self.setup_frame.pack_forget()
            json_manager.save_data(self.data)

    def change_keybind(self):
        # Create a popup window for keybind assignment
        popup = tk.Toplevel(self)
        popup.title("Change Keybind")

        current_keybind = self.button_data.get("keybind", "")
        if current_keybind.isalpha() and len(current_keybind) == 1:
            current_keybind = current_keybind.upper()  # Show in uppercase if it's a letter

        label = tk.Label(popup, text=f"Current Keybind: {current_keybind}", fg="blue")
        label.pack(pady=10)

        info_label = tk.Label(popup, text="Press a new key or click 'Clear Keybind'.")
        info_label.pack(pady=10)

        clear_button = tk.Button(popup, text="Clear Keybind", command=lambda: self.clear_keybind(popup))
        clear_button.pack(pady=5)

        confirm_button = tk.Button(popup, text="Confirm", command=lambda: self.confirm_keybind(popup))
        confirm_button.pack(side="left", padx=(20, 5), pady=5)

        cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy)
        cancel_button.pack(side="right", padx=(5, 20), pady=5)

        popup.bind('<KeyPress>', lambda event: self.update_keybind(event, label))

        popup.focus_set()  # Set focus to the popup to capture key events

    def update_keybind(self, event, label):
        # Update the label with the new key pressed
        new_key = event.keysym
        if new_key.isalpha() and len(new_key) == 1:
            new_key = new_key.upper()  # Show in uppercase if it's a letter

        label.config(text=f"Current Keybind: {new_key}")  # Update displayed keybind
        self.new_keybind = new_key  # Store the new key for confirmation

    def clear_keybind(self, popup):
        self.button_data["keybind"] = ""  # Clear the keybind in button data
        self.update_label()  # Update label to reflect changes
        popup.destroy()  # Close the popup

    def confirm_keybind(self, popup):
        self.button_data["keybind"] = getattr(self, 'new_keybind', "").upper()  # Store as uppercase
        self.update_label()  # Update label to reflect changes
        json_manager.save_data(self.data)  # Save updated data
        popup.destroy()  # Close the popup


