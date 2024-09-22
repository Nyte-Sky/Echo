import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json_manager  # Assuming you have this module for handling JSON
import audio_manager  # Assuming you have this module for playing audio

class SetupTab(ttk.Frame):
    def __init__(self, parent, button_data_list, data, keylist):
        super().__init__(parent)
        self.button_data_list = button_data_list  # List of button data dictionaries
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

        self.setup_frames = []  # To hold individual button setup frames

        # Create a setup frame for each button
        for button_data in self.button_data_list:
            setup_frame = tk.Frame(main_area, bg="lightgray", width=120, height=50, relief="solid", bd=1)
            setup_frame.pack(padx=10, pady=10, fill="x")  # Pack with padding

            label_text = button_data['name']
            keybind_display = button_data.get("keybind", "")

            # Create the button name label
            label = tk.Label(setup_frame, text=label_text, bg="lightgray")
            label.pack(side="left", padx=5)

            if True:
                # Convert to uppercase if it's a regular letter (A-Z)
                if keybind_display.isalpha() and len(keybind_display) == 1:
                    keybind_display = keybind_display.upper()

                # Create the keybind label in blue
                keybind_label = tk.Label(setup_frame, text=keybind_display, bg="lightgray", fg="blue")
                keybind_label.pack(side="left")  # Display keybind in blue

            # Store the setup frame and its related data
            self.setup_frames.append((setup_frame, button_data, label, keybind_label))

            # Create dropdown menu for each button
            dropdown_var = tk.StringVar(setup_frame)
            dropdown_var.set("\u22EF")  # Unicode character for three dots (⋅⋅⋅)
            self.create_dropdown(setup_frame, dropdown_var, button_data)

    def create_dropdown(self, setup_frame, dropdown_var, button_data):
        dropdown_menu = ttk.OptionMenu(setup_frame, dropdown_var, "\u22EF",
                                         "Change sound", "Rename", "Delete", "Change Keybind", "Change Volume",
                                         command=lambda action: self.dropdown_action(action, button_data, dropdown_var))
        dropdown_menu.pack(side="right", padx=10)

    def dropdown_action(self, action, button_data, dropdown):
        if action == "Change sound":
            self.change_sound(button_data)
        elif action == "Rename":
            self.rename_button(button_data)
        elif action == "Delete":
            self.delete_button(button_data)
        elif action == "Change Keybind":
            self.change_keybind(button_data)
        elif action == "Change Volume":
            self.change_volume(button_data)
        
        dropdown.set("\u22EF")

    def change_volume(self, button_data):
        # Create a popup window for volume assignment
        popup = tk.Toplevel(self)
        popup.title("Change Volume")
        popup.geometry("230x125")
        current_volume = button_data.get("volume", "")

        volume_scale = tk.Scale(popup, from_=0, to=10, orient="horizontal")
        volume_scale.set(current_volume * 10)  # Assuming volume is stored as a fraction (0.0 - 1.0)
        volume_scale.pack()

        play_button = tk.Button(popup, text="Play", command=lambda: audio_manager.play_audio(button_data["sound_path"], volume_scale.get() / 10))
        play_button.pack(pady=5)

        confirm_button = tk.Button(popup, text="Confirm", command=lambda: self.confirm_volume(popup, button_data, volume_scale.get() / 10))
        confirm_button.pack(side="left", padx=(20, 5), pady=5)

        cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy)
        cancel_button.pack(side="right", padx=(5, 20), pady=5)

    def confirm_volume(self, popup, button_data, current_volume):
        button_data["volume"] = current_volume
        json_manager.save_data(self.data)  # Save updated data
        popup.destroy()  # Close the popup

    def change_sound(self, button_data):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg"), ("All Files", "*.*")])
        if file_path:
            button_data["sound_path"] = file_path
            json_manager.save_data(self.data)
            messagebox.showinfo("Success", "Sound changed successfully!")

    def rename_button(self, button_data):
        new_name = simpledialog.askstring("Rename Button", "Enter new name:")
        if new_name:
            button_data["name"] = new_name
            for setup_frame, bd, label, keybind_label in self.setup_frames:
                if bd == button_data:
                    label.config(text=new_name)  # Update label display
                    break
            json_manager.save_data(self.data)

    def delete_button(self, button_data):
        result = messagebox.askyesno("Delete Button", "Are you sure you want to delete this button?")
        if result:
            self.data["buttons"].remove(button_data)
            for setup_frame, bd, label, keybind_label in self.setup_frames:
                if bd == button_data:
                    setup_frame.pack_forget()  # Remove the setup frame
                    break
            json_manager.save_data(self.data)

    def change_keybind(self, button_data):
        # Create a popup window for keybind assignment
        popup = tk.Toplevel(self)
        popup.title("Change Keybind")
        popup.geometry("260x175")

        current_keybind = button_data.get("keybind", "")
        if current_keybind.isalpha() and len(current_keybind) == 1:
            current_keybind = current_keybind.upper()  # Show in uppercase if it's a letter

        label = tk.Label(popup, text=f"Current Keybind: {current_keybind}", fg="blue")
        label.pack(pady=5)

        clashLabel = tk.Label(popup, text="", fg="red")
        clashLabel.pack()

        info_label = tk.Label(popup, text="Press a new key or click 'Clear Keybind'.")
        info_label.pack(pady=5)

        clear_button = tk.Button(popup, text="Clear Keybind", command=lambda: self.clear_keybind(popup, label, button_data))
        clear_button.pack(pady=5)

        confirm_button = tk.Button(popup, text="Confirm", command=lambda: self.confirm_keybind(popup, button_data))
        confirm_button.pack(side="left", padx=(20, 5), pady=5)

        cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy)
        cancel_button.pack(side="right", padx=(5, 20), pady=5)

        popup.bind('<KeyPress>', lambda event: self.update_keybind(event, label, clashLabel, button_data))

        popup.focus_set()  # Set focus to the popup to capture key events

    def get_used_keybinds(self):
        keybinds = []
        for button in self.button_data_list:
            keybind = button.get("keybind")
            if keybind and keybind not in keybinds:  # Check if keybind is not empty and not already in the list
                keybinds.append(keybind)
        return keybinds

    def check_if_keybind_is_valid(self, keybind, button_data):
        used_keybinds = self.get_used_keybinds()
        return (keybind in used_keybinds and not keybind == button_data["keybind"])
        

    def update_keybind(self, event, label, clashLabel, button_data):
        # Update the label with the new key pressed
        new_key = event.keysym

        if self.check_if_keybind_is_valid(new_key.upper(), button_data):
            self.valid_key = False
            clashLabel.config(text="This keybind is already in use.")
        else:
            self.valid_key = True
            clashLabel.config(text="")

        if new_key.isalpha() and len(new_key) == 1:
            new_key = new_key.upper()  # Show in uppercase if it's a letter

        label.config(text=f"Current Keybind: {new_key}")  # Update displayed keybind
        self.new_keybind = new_key

    def clear_keybind(self, popup, label, button_data):
        # Update the label with the new key pressed
        new_key = ""

        label.config(text=f"Current Keybind: {new_key}")  # Update displayed keybind
        self.new_keybind = new_key

    def confirm_keybind(self, popup, button_data):
        button_data["keybind"] = getattr(self, 'new_keybind', "").upper()  # Store as uppercase
        for setup_frame, bd, label, keybind_label in self.setup_frames:
            if bd == button_data:
                keybind_label.config(text=button_data["keybind"])  # Update displayed keybind
                break
        json_manager.save_data(self.data)  # Save updated data
        popup.destroy()  # Close the popup



