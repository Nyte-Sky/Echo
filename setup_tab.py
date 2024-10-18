import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json_manager  # Assuming you have this module for handling JSON
import audio_manager  # Assuming you have this module for playing audio
from PIL import Image, ImageTk  # Import Pillow for image handling
import os

class SetupTab(ttk.Frame):
    def __init__(self, parent, button_data_list, settings_data, data, keylist, board_tab):
        super().__init__(parent)
        self.settings_data = settings_data
        self.button_data_list = button_data_list
        self.data = data
        self.key_list = keylist
        self.board_tab = board_tab

        self.image_vis = tk.BooleanVar(value=settings_data["bg-images-shown"])

        main_area, top_bar, bottom_bar = self.create_fund_widgets()

        # Instantiate manager classes
        self.image_manager = ImageManager(settings_data, self.image_vis, main_area, top_bar, button_data_list, board_tab, self.data, self)
        self.button_manager = ButtonManager(self, button_data_list, board_tab, self, self.settings_data, self.data)
        self.volume_manager = VolumeManager(audio_manager, json_manager, data, self)

        self.image_manager.setup_image()
        self.create_frames()
        self.create_other_widgets()

    # Delegate image-related functions to ImageManager
    def reload_bg_image(self):
        self.image_manager.reload_bg_image()

    def create_fund_widgets(self):
        self.top_bar = tk.Frame(self, height=20, bg="lightgray")
        self.top_bar.pack(side="top", fill="x")

        self.main_area = tk.Frame(self, bg="white", width=500, height=300)
        self.main_area.pack(expand=True, fill="both")

        self.bottom_bar = tk.Frame(self, height=20, bg="lightgray")
        self.bottom_bar.pack(side="bottom", fill="x")

        return self.main_area, self.top_bar, self.bottom_bar

    def create_frames(self):
        self.setup_frames = []  # To hold individual button setup frames

        class Borders():
            def __init__(self, root) -> None:
                self.black_border = tk.Frame(root, background="black", width=120, height=50)
                self.red_border = tk.Frame(root, background="red", width=120, height=50)
                self.blue_border = tk.Frame(root, background="blue", width=120, height=50)
            
        def valid_file_path( button_data):
            return os.path.exists(button_data["sound_path"])

        # Create a setup frame for each button
        for button_data in self.button_data_list:
            # print(button_data)
            # border_frame = Borders(self.main_area).black_border if valid_file_path(button_data) else Borders(self.main_area).red_border
            # border_frame.pack(padx=10, pady=10, fill="x")

            setup_frame = tk.Frame(self.main_area, bg="#e6e6e6", width=120, height=50, relief="solid", bd=1)
            setup_frame.pack(padx=10, pady=10, fill="x")  # Pack with padding

            label_text = button_data['name']
            keybind_display = button_data.get("keybind", "")

            # Create the button name label
            label = tk.Label(setup_frame, text=label_text, bg="#e6e6e6")
            label.pack(side="left", padx=5)

            # Convert to uppercase if it's a regular letter (A-Z)
            if keybind_display.isalpha() and len(keybind_display) == 1:
                keybind_display = keybind_display.upper()
            
            if keybind_display != "":
                # Create the keybind label in blue
                keybind_label = tk.Label(setup_frame, text=keybind_display, bg="#e6e6e6", fg="blue")
                keybind_label.pack(side="left")  # Display keybind in blue

            if not valid_file_path(button_data):
                test_label = tk.Label(setup_frame, text="Invalid sound path", bg="#e6e6e6", fg="red")
                test_label.pack(side="left", padx=5)
            
            # Store the setup frame and its related data
            self.setup_frames.append((setup_frame, button_data, label, keybind_label, None))

            # Create dropdown menu for each button
            dropdown_var = tk.StringVar(setup_frame)
            dropdown_var.set("\u22EF")  # Unicode character for three dots (⋅⋅⋅)
            self.create_dropdown(setup_frame, dropdown_var, button_data)
            # end for loop
        
        add_button = tk.Button(self.main_area, bg="#e6e6e6", text="\uff0b", 
                               fg="blue", width=4, height=1, relief="solid", 
                               bd=1, command = lambda: self.button_manager.add_button())
        add_button.pack(padx=10, pady=10, anchor="w")  # Pack with padding
        self.setup_frames.append((add_button, None, None, None, None))
    
    def create_other_widgets(self):

        # Create a Label for the text
        image_label = tk.Button(self.top_bar, text="Background Image: \u2713" if self.image_vis.get() else "Background Image: \u2717", 
                                bg="#e6e6e6", relief="solid", bd=1,
                                command=lambda: self.image_manager.bg_image_toggle(image_label))
        image_label.pack(side=tk.LEFT)  # Place the text on the left

        # Select image button
        change_image_button = tk.Button(self.top_bar, text="Change image", bg="#e6e6e6", relief="solid", bd=1, command=lambda: self.image_manager.change_image_popup())
        change_image_button.pack(side=tk.LEFT)

        muted_checkbox = tk.Button(self.top_bar, text="Muted: " + ("\u2717" if self.board_tab.allow_keypresses else "\u2713"),
                                bg="#e6e6e6", relief="solid", bd=1, pady=0,
                                command=lambda: self.toggle_mute(muted_checkbox))
        muted_checkbox.pack(side=tk.RIGHT)

        oof_key_sim = tk.Button(self.top_bar, text="Listen for keybinds while windowed: " + ("\u2713" if self.board_tab.oof_key_sims else "\u2717"),
                                bg="#e6e6e6", relief="solid", bd=1, pady=0,
                                command=lambda: self.toggle_oof_key_sim(oof_key_sim))
        oof_key_sim.pack(side=tk.RIGHT)
               
    def toggle_oof_key_sim(self, button):
        self.board_tab.oof_key_sims = not self.board_tab.oof_key_sims
        self.settings_data["out-of-focus-input"] = self.board_tab.oof_key_sims
        json_manager.save_data(self.data)
        button.config(text="Listen for keybinds while windowed: " + ("\u2713" if self.board_tab.oof_key_sims else "\u2717"))
               
    def toggle_mute(self, button):
        self.board_tab.allow_keypresses = not self.board_tab.allow_keypresses
        button.config(text="Muted: " + ("\u2717" if self.board_tab.allow_keypresses else "\u2713"))

    def create_dropdown(self, setup_frame, dropdown_var, button_data):
        dropdown_menu = ttk.OptionMenu(setup_frame, dropdown_var, "\u22EF",
                                         "Sound", "Keybind", "Volume", "Type", "Rename", "Delete", 
                                         command=lambda action: self.dropdown_action(action, button_data, dropdown_var))
        dropdown_menu.pack(side="right", padx=1)

    def dropdown_action(self, action, button_data, dropdown):
        if action == "Sound":
            self.button_manager.change_sound(button_data)
        elif action == "Rename":
            self.button_manager.rename_button(button_data)
        elif action == "Delete":
            self.button_manager.delete_button(button_data)
        elif action == "Keybind":
            self.button_manager.change_keybind(button_data)
        elif action == "Volume":
            self.volume_manager.change_volume(button_data)
        elif action == "Appearance":
            self.button_manager.change_appearance(button_data)
        elif action == "Type":
            self.button_manager.change_type(button_data)
        
        dropdown.set("\u22EF")
    
class TypeChange(tk.Toplevel):
    def __init__(self, root_window, button_data, data):
        super().__init__(root_window)
        self.button_data = button_data
        self.data = data

        # Variable to hold the selection of the radio buttons
        self.selected_option = tk.StringVar(value=button_data["type"])  # Default value
        
        # Create two radio buttons (mutually exclusive)
        self.radio1 = tk.Radiobutton(self, text="Short - Plays once until finished, will overlap", variable=self.selected_option, value="short")
        self.radio1.pack(pady=(5,0))
        
        self.radio2 = tk.Radiobutton(self, text="Long - Plays until clicked again or finished, will not overlap", variable=self.selected_option, value="long")
        self.radio2.pack(pady=(0,5))

        self.radio3 = tk.Radiobutton(self, text="Repeat - Repeats until clicked again, will not overlap", variable=self.selected_option, value="repeat")
        self.radio3.pack(pady=(0,5))
    
        self.radio4 = tk.Radiobutton(self, text="Music - Plays looped until other music button is clicked, will not overlap", variable=self.selected_option, value="music")
        self.radio4.pack(pady=(0,5))
        
        # Create Confirm and Cancel buttons
        self.confirm_button = tk.Button(self, text="Confirm", command=self.on_confirm)
        self.confirm_button.pack(pady=5)
        
        self.cancel_button = tk.Button(self, text="Cancel", command=self.on_cancel)
        self.cancel_button.pack(pady=5)

    def on_confirm(self):
        # Handle the confirm action (print or pass the selected value)
        choice = self.selected_option.get()
        self.button_data["type"] = choice
        audio_manager.stop_continuous_audio(self.button_data["sound_path"])
        json_manager.save_data(self.data)
        self.destroy()  # Close the window

    def on_cancel(self):
        self.destroy()  # Close the window when cancel is clicked
    
class AppearenceChange(tk.Toplevel):
    def __init__(self, root_window, button_data, data):
        super().__init__(root_window)
        self.button_data = button_data
        self.data = data
        self.styles = json_manager.load_styles()

        self.title("Change Appearance")
        self.geometry("400x260")

        # Create and configure the button widget in the popup
        self.appearance_button = ttk.Button(self, style=button_data["style"], text=button_data["name"])
        self.appearance_button.pack(anchor="center", padx=5, pady=5)

        self.appearance_style_frame = tk.Frame(self)
        self.appearance_style_frame.pack(anchor="center")

        # Create a label for the style
        self.style_label = tk.Label(self.appearance_style_frame, text="Style: ")
        self.style_label.pack(side=tk.LEFT, padx=0)

        # Dropdown menu for style options
        self.appearance_dropdown_var = tk.StringVar()  # Create a StringVar to track the selected option
        self.style_dropdown = ttk.OptionMenu(self.appearance_style_frame, self.appearance_dropdown_var, button_data["style"],
                                            *[style["name"] for style in self.styles], "New",
                                            command=lambda action: self.appearance_dropdown_action(action))
        self.style_dropdown.pack(side=tk.LEFT, padx=0)

        # Set focus to the popup window
        self.focus()

    def appearance_dropdown_action(self, style):
        if style.lower() == "new":
            return
        self.appearance_button.config(style=style)



class sidebysidewidgets(tk.Frame):
    def __init__(self, parent, widgets=None):
        super.__init__(parent)
        if widgets: self.add_widgets(widgets)
    
    def add_widgets(self, widgets: list[tk.Widget]):
        for widget in widgets:
            widget.pack(side=tk.LEFT, padx=0)

class VolumeManager:
    def __init__(self, audio_manager, json_manager, data, root_win):
        self.audio_manager = audio_manager
        self.json_manager = json_manager
        self.data = data
        self.root_window = root_win

    def change_volume(self, button_data):
        # Create a popup window for volume assignment
        popup = tk.Toplevel(self.root_window)
        popup.title("Change Volume")
        popup.geometry("230x125")
        current_volume = button_data.get("volume", "")

        volume_scale = tk.Scale(popup, from_=0, to=10, orient="horizontal")
        volume_scale.set(current_volume * 10)  # Assuming volume is stored as a fraction (0.0 - 1.0)
        volume_scale.pack()

        play_button = tk.Button(popup, text="Play", command=lambda: audio_manager.play_continuous_audio(button_data["sound_path"], volume_scale.get() / 10))
        play_button.pack(pady=5)

        confirm_button = tk.Button(popup, text="Confirm", command=lambda: self.confirm_volume(popup, button_data, volume_scale.get() / 10))
        confirm_button.pack(side="left", padx=(20, 5), pady=5)

        cancel_button = tk.Button(popup, text="Cancel", command=lambda: self.cancel(button_data, popup))
        cancel_button.pack(side="right", padx=(5, 20), pady=5)
    
    def cancel(self, button_data, popup: tk.Toplevel):
        audio_manager.stop_continuous_audio(button_data["sound_path"])
        popup.destroy()

    def confirm_volume(self, popup, button_data, new_volume):
        audio_manager.stop_continuous_audio(button_data["sound_path"])
        button_data["volume"] = new_volume
        self.json_manager.save_data(self.data)  # Save updated data
        popup.destroy()  # Close the popup

class ButtonManager:
    def __init__(self, setup_tab, button_data_list, board_tab, root_win, settings_data, data):
        self.setup_tab = setup_tab
        self.button_data_list = button_data_list
        self.settings_data = settings_data
        self.data = data
        self.board_tab = board_tab
        self.root_window = root_win
        
        self.keybind_widgets = {}
        self.appearance_widgets = {}

    def add_button(self):
        button_data = {
            "name": "",
            "sound_path": "",
            "volume": 0.5,
            "style": "Square.TButton",
            "keybind": ""
        }
        self.button_data_list.append(button_data)
        name = simpledialog.askstring("Enter Name", "New Button Name:")
        if not name:
            return
        button_data["name"] = name
        json_manager.save_data(self.data)
        self.update_setup_frame()
        self.board_tab.update_buttons()

    def rename_button(self, button_data):
        new_name = simpledialog.askstring("Rename Button", "Enter new name:")
        if new_name:
            button_data["name"] = new_name
            json_manager.save_data(self.data)
            self.update_setup_frame()
            self.board_tab.update_buttons()  # Refresh buttons in BoardTab

    def update_setup_frame(self):
        for frame, _, _, _, border_frame in self.setup_tab.setup_frames:
            frame.destroy()
            if border_frame:
                border_frame.destroy()
        self.setup_tab.create_frames()
        
    def change_sound(self, button_data):
        file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
        if file_path:
            button_data["sound_path"] = file_path
            self.update_setup_frame()
            json_manager.save_data(self.data)
            
    def change_appearance(self, button_data):
        AppearenceChange(self.root_window, button_data, self.data)

    def delete_button(self, button_data):
        result = messagebox.askyesno("Delete Button", "Are you sure you want to delete this button?")
        if result:
            self.data["buttons"].remove(button_data)
            for setup_frame, bd, _, _, border_frame in self.setup_tab.setup_frames:
                if bd == button_data:
                    setup_frame.destroy()  # Remove the setup frame
                    if border_frame:
                        border_frame.destroy()
                    self.board_tab.update_buttons()
                    break
            json_manager.save_data(self.data)
    
    def change_type(self, button_data):
        TypeChange(self.root_window, button_data, self.data)

    def change_keybind(self, button_data):
        # Create a popup window for keybind assignment
        self.popup = tk.Toplevel(self.root_window)
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
    
    def confirm_keybind(self):
        # Save the new keybind in button data
        self.button_data["keybind"] = self.new_keybind.upper()  # Store as uppercase

        # Update keybind label in the corresponding setup frame
        for _, bd, _, keybind_label, _ in self.setup_tab.setup_frames:
            if bd == self.button_data:
                keybind_label.config(text=self.button_data["keybind"])
                break
                # Save updated data and close the popup
        
        json_manager.save_data(self.data)
        self.popup.destroy()
    
    def clear_keybind(self):
        # Clear the keybind and update UI
        self.new_keybind = ""
        self.keychange_widgets['keybind_label'].config(text=f"Current Keybind: {self.new_keybind}")
        self.update_keybind(self.MockEvent(""))

    # Mock event to simulate clearing the keybind
    class MockEvent:
        def __init__(self, keysym, fake=False):
            self.keysym = keysym
            self.fake = fake

    def update_keybind(self, event):
        new_key = event.keysym.upper()
        # Check if the new keybind is already in use
        if self.check_keybind_conflict(new_key):
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

    def check_keybind_conflict(self, new_key):
        used_keybinds = self.get_used_keybinds()
        return new_key in used_keybinds
    
    def get_used_keybinds(self):
        return [btn["keybind"] for btn in self.button_data_list if btn.get("keybind")]

class ImageManager:
    def __init__(self, settings_data, image_vis_var, main_area, top_bar, button_data_list, board_tab, data, root_win):
        self.settings_data = settings_data
        self.button_data_list = button_data_list
        self.data = data
        self.root_window = root_win

        self.image_vis = image_vis_var
        self.board_tab = board_tab

        self.main_area = main_area
        self.top_bar = top_bar
        
        # Initialize image variables
        self.original_image = None
        self.resized_image = None
        self.image_label = None

    def bg_image_toggle(self, image_label):
        self.image_vis.set(not self.image_vis.get())
        self.settings_data["bg-images-shown"] = self.image_vis.get()
        json_manager.save_data(self.data)
        self.reload_bg_image()
        self.board_tab.reload_bg_image()
        image_label.config(text="Background Image: \u2713" if self.image_vis.get() else "Background Image: \u2717")

    def change_image_popup(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("All Files", "*.*")])
        if file_path:
            popup = tk.Toplevel(self.root_window)
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

    def setup_image(self, fixed_size=(200, 200)):
        if self.settings_data["setup-bg-image-path"] != "":
            self.original_image = Image.open(self.settings_data["setup-bg-image-path"])
        else:
            self.original_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))  # Fully transparent
        self.resized_image = self.original_image.resize(fixed_size)
        self.image = ImageTk.PhotoImage(self.resized_image)
        self.image_label = tk.Label(self.main_area, image=self.image, bg="white")
        self.image_label.place(relx=1.0, rely=1.0, anchor="se", x=20)  # Place in bottom-right corner
    
    def reload_bg_image(self, forced=False):
        if self.image_vis.get() or forced:
            if self.settings_data["setup-bg-image-path"] != "":
                self.original_image = Image.open(self.settings_data["setup-bg-image-path"])
            else:
                self.original_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))  # Fully transparent
            self.resized_image = self.original_image.resize((200, 200))
            self.image = ImageTk.PhotoImage(self.resized_image)
            if self.image_label:
                self.image_label.config(image=self.image)
        else:
            self.clear_image()

    def clear_image(self):
        self.original_image = None
        self.resized_image = None
        self.image = None
        if self.image_label:
            self.image_label.config(image="")
