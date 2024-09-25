import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json_manager  # Assuming you have this module for handling JSON
import audio_manager  # Assuming you have this module for playing audio
from PIL import Image, ImageTk  # Import Pillow for image handling

class SetupTab(ttk.Frame):
    def __init__(self, parent, button_data_list, settings_data, data, keylist, board_tab):
        super().__init__(parent)
        self.button_data_list = button_data_list  # List of button data dictionaries
        self.settings_data = settings_data
        self.image_vis = tk.BooleanVar(value=settings_data["bg-images-shown"])
        self.board_bg_image_path = settings_data["board-bg-image-path"]
        self.setup_bg_image_path = settings_data["setup-bg-image-path"]
        self.data = data
        self.board_tab = board_tab
        self.keylist = keylist  # Store keylist for reference
        # self.create_widgets()
        self.create_fund_widgets()
        self.setup_image()
        self.image_label.place(relx=1.0, rely=1.0, anchor="se", x=20)  # Place in bottom-right corner
        self.create_widgets()
        # self.bind("<Configure>", self.on_resize)

    def setup_image(self, fixed_size=(200, 200)):
        """Load and optionally resize the image to be displayed in the bottom-right corner."""

        if True:
            # Load the original image
            self.original_image = Image.open(self.settings_data["setup-bg-image-path"])
            self.resized_image = self.original_image.resize(fixed_size)

            # Convert the image to a PhotoImage object to display in Tkinter
            self.image = ImageTk.PhotoImage(self.resized_image)
            self.image_label = tk.Label(self.main_area, image=self.image, bg="white")
            self.reload_bg_image()
    
    def reload_bg_image(self, forced=False):
        # print(self.image_vis.get())
        if self.image_vis.get() or forced:
            self.original_image = Image.open(self.settings_data["setup-bg-image-path"])
            self.resized_image = self.original_image.resize((200, 200))
            self.image = ImageTk.PhotoImage(self.resized_image)
            # self.image_label = tk.Label(self.main_area, image=self.image, bg="white")
            self.image_label.config(image=self.image)
            # print("Reloading image - (re)showing")
        else:
            self.original_image = None
            self.resized_image = None
            self.image = None
            #self.image_label = None
            # print("Reloading image - (re)setting image to none")

    def bg_image_toggle(self, image_label):
        self.image_vis.set(not self.image_vis.get())
        self.settings_data["bg-images-shown"] = self.image_vis.get()
        json_manager.save_data(self.data)
        self.reload_bg_image()
        self.board_tab.reload_bg_image()
        image_label.config(text="Background Image: \u2713" if self.image_vis.get() else "Background Image: \u2717")

    def create_fund_widgets(self):
        self.top_bar = tk.Frame(self, height=20, bg="lightgray")
        self.top_bar.pack(side="top", fill="x")

        self.main_area = tk.Frame(self, bg="white", width=500, height=300)
        self.main_area.pack(expand=True, fill="both")

        self.bottom_bar = tk.Frame(self, height=20, bg="lightgray")
        self.bottom_bar.pack(side="bottom", fill="x")

    def create_widgets(self):
        self.setup_frames = []  # To hold individual button setup frames

        # Create a setup frame for each button
        for button_data in self.button_data_list:
            setup_frame = tk.Frame(self.main_area, bg="#e6e6e6", width=120, height=50, relief="solid", bd=1)
            setup_frame.pack(padx=10, pady=10, fill="x")  # Pack with padding

            label_text = button_data['name']
            keybind_display = button_data.get("keybind", "")

            # Create the button name label
            label = tk.Label(setup_frame, text=label_text, bg="#e6e6e6")
            label.pack(side="left", padx=5)

            if True:
                # Convert to uppercase if it's a regular letter (A-Z)
                if keybind_display.isalpha() and len(keybind_display) == 1:
                    keybind_display = keybind_display.upper()

                # Create the keybind label in blue
                keybind_label = tk.Label(setup_frame, text=keybind_display, bg="#e6e6e6", fg="blue")
                keybind_label.pack(side="left")  # Display keybind in blue

            # Store the setup frame and its related data
            self.setup_frames.append((setup_frame, button_data, label, keybind_label))

            # Create dropdown menu for each button
            dropdown_var = tk.StringVar(setup_frame)
            dropdown_var.set("\u22EF")  # Unicode character for three dots (⋅⋅⋅)
            self.create_dropdown(setup_frame, dropdown_var, button_data)

        # Create top bar widgets

        # Create a frame to hold the Checkbutton and the text'''
        '''check_frame = tk.Frame(self.top_bar, bg="#e6e6e6", relief="solid", bd=1)
        check_frame.pack(side=tk.LEFT)'''
    
        # Create a Label for the text
        image_label = tk.Button(self.top_bar, text="Background Image: \u2713" if self.image_vis.get() else "Background Image: \u2717", 
                                bg="#e6e6e6", relief="solid", bd=1,
                                command=lambda: self.bg_image_toggle(image_label))
        image_label.pack(side=tk.LEFT)  # Place the text on the left

        # Select image button
        change_image_button = tk.Button(self.top_bar, text="Change image", bg="#e6e6e6", relief="solid", bd=1, command=lambda: self.change_image_popup())
        change_image_button.pack(side=tk.LEFT)

    def change_image_popup(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")])
        if file_path:
            popup = tk.Toplevel(self)
            popup.title("Change Image")
            popup.geometry("150x100")
            selection = tk.StringVar()
            msg = tk.Label(popup, text="Change for: ")
            msg.pack()
            selection_dropdown = ttk.OptionMenu(popup, selection, "Both", "Both", "Board Only", "Setup Only")
            selection_dropdown.pack()
            confirm_button = tk.Button(popup, text="Confirm", command=lambda: self.change_image_confirm(file_path, selection, popup))
            confirm_button.pack(side="left", padx=(20, 5), pady=5)

            cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy)
            cancel_button.pack(side="right", padx=(5, 20), pady=5)

    def change_image_confirm(self, image_path, selection, popup):
        # print(type(selection.get()))
        if selection.get() == "Both":
            # print("changing")
            self.settings_data["setup-bg-image-path"] = image_path
            self.settings_data["board-bg-image-path"] = image_path
            self.board_tab.reload_bg_image()
            self.reload_bg_image()
        elif selection.get() == "Board Only":
            self.settings_data["board-bg-image-path"] = image_path
            self.board_tab.reload_bg_image()
        elif selection.get() == "Setup Only":
            self.settings_data["setup-bg-image-path"] = image_path
            self.reload_bg_image()
        json_manager.save_data(self.data)  # Save updated data
        popup.destroy()  # Close the popup

    def create_dropdown(self, setup_frame, dropdown_var, button_data):
        dropdown_menu = ttk.OptionMenu(setup_frame, dropdown_var, "\u22EF",
                                         "Change sound", "Change Keybind", "Change Volume", "Rename", "Delete",
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

            # Call the update method in BoardTab to refresh button names
            self.board_tab.update_buttons()  # Update button names in the BoardTab

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

        self.clashLabel = tk.Label(popup, text="", fg="red")
        self.clashLabel.pack()

        info_label = tk.Label(popup, text="Press a new key or click 'Clear Keybind'.")
        info_label.pack(pady=5)

        clear_button = tk.Button(popup, text="Clear Keybind", command=lambda: self.clear_keybind(popup, label, button_data))
        clear_button.pack(pady=5)

        confirm_button = tk.Button(popup, text="Confirm", command=lambda: self.confirm_keybind(popup, button_data))
        confirm_button.pack(side="left", padx=(20, 5), pady=5)

        cancel_button = tk.Button(popup, text="Cancel", command=popup.destroy)
        cancel_button.pack(side="right", padx=(5, 20), pady=5)

        popup.bind('<KeyPress>', lambda event: self.update_keybind(event, label, button_data, popup.winfo_children()))

        popup.focus_set()  # Set focus to the popup to capture key events

    def get_used_keybinds(self):
        keybinds = []
        for button in self.button_data_list:
            keybind = button.get("keybind")
            if keybind:  # Check if keybind is not empty
                keybinds.append(keybind)
        return keybinds

    def check_if_keybind_is_valid(self, keybind, button_data):
        used_keybinds = self.get_used_keybinds()
        print(used_keybinds)
        print(keybind)
        if button_data["keybind"] in used_keybinds:
            used_keybinds.remove(button_data["keybind"])
        print(used_keybinds)
        return keybind in used_keybinds
        
    def change_keybind(self, button_data):
        # Create a popup window for keybind assignment
        self.popup = tk.Toplevel(self)
        self.popup.title("Change Keybind")
        self.popup.geometry("260x175")

        # Store button data and popup widget
        self.button_data = button_data

        # Initialize dictionary to store keybind-related widgets
        self.keychange_widgets = {}

        current_keybind = button_data.get("keybind", "")
        if current_keybind.isalpha() and len(current_keybind) == 1:
            current_keybind = current_keybind.upper()  # Show in uppercase if it's a letter

        # Store all relevant widgets in the keychange_widgets dictionary
        self.keychange_widgets['keybind_label'] = tk.Label(self.popup, text=f"Current Keybind: {current_keybind}", fg="blue")
        self.keychange_widgets['keybind_label'].pack(pady=5)

        self.keychange_widgets['clash_label'] = tk.Label(self.popup, text="", fg="red")
        self.keychange_widgets['clash_label'].pack()

        info_label = tk.Label(self.popup, text="Press a new key or click 'Clear Keybind'.")
        info_label.pack(pady=5)

        clear_button = tk.Button(self.popup, text="Clear Keybind", command=self.clear_keybind)
        clear_button.pack(pady=5)

        self.keychange_widgets["confirm_button"] = tk.Button(self.popup, text="Confirm", command=self.confirm_keybind)
        self.keychange_widgets["confirm_button"].pack(side="left", padx=(20, 5), pady=5)

        cancel_button = tk.Button(self.popup, text="Cancel", command=self.popup.destroy)
        cancel_button.pack(side="right", padx=(5, 20), pady=5)

        # Bind keypress event to the popup window
        self.popup.bind('<KeyPress>', self.update_keybind)

        self.popup.focus_set()  # Set focus to the popup to capture key events

    def get_used_keybinds(self):
        keybinds = [button.get("keybind") for button in self.button_data_list if button.get("keybind")]
        return keybinds

    def check_if_keybind_is_valid(self, keybind):
        used_keybinds = self.get_used_keybinds()
        if self.button_data["keybind"] in used_keybinds:
            used_keybinds.remove(self.button_data["keybind"])
        return keybind in used_keybinds

    def update_keybind(self, event):
        # Update the label with the new key pressed
        new_key = event.keysym.upper()  # Always store as uppercase

        # Check if the new keybind is already in use
        if self.check_if_keybind_is_valid(new_key):
            self.valid_key = False
            self.keychange_widgets['clash_label'].config(text="This keybind is already in use.")
            self.keychange_widgets["confirm_button"].config(state="disabled")
        else:
            self.valid_key = True
            self.keychange_widgets['clash_label'].config(text="")
            self.keychange_widgets["confirm_button"].config(state="normal")

        # Update displayed keybind
        self.keychange_widgets['keybind_label'].config(text=f"Current Keybind: {new_key}")
        self.new_keybind = new_key

    def clear_keybind(self):
        # Mock event to simulate clearing the keybind
        class MockEvent:
            def __init__(self, keysym):
                self.keysym = keysym

        # Clear the keybind and update UI
        self.new_keybind = ""
        self.keychange_widgets['keybind_label'].config(text=f"Current Keybind: {self.new_keybind}")
        self.update_keybind(MockEvent(""))

    def confirm_keybind(self):
        # Save the new keybind in button data
        self.button_data["keybind"] = self.new_keybind.upper()  # Store as uppercase

        # Update keybind label in the corresponding setup frame
        for setup_frame, bd, label, keybind_label in self.setup_frames:
            if bd == self.button_data:
                keybind_label.config(text=self.button_data["keybind"])
                break

        # Save updated data and close the popup
        json_manager.save_data(self.data)
        self.popup.destroy()

