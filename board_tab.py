import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Import Pillow for image handling
import audio_manager
from styles import configure_button_styles

class BoardTab(ttk.Frame):
    def __init__(self, parent, button_data_list, settings_data):
        super().__init__(parent)
        self.button_data_list = button_data_list  # List of button data entries
        self.settings_data = settings_data
        self.show_bg_image = bool(settings_data["bg-images-shown"])
        configure_button_styles()
        self.image_path = settings_data["board-bg-image-path"]
        self.setup_image()
        self.image_label.place(relwidth=1, relheight=1)  # Show the background image
        self.create_widgets()
        self.allow_keypresses = True
        self.bind('<KeyPress>', self.handle_keypress)
        self.bind("<Configure>", self.resize_background)  # Bind the configure event to resize background
        self.oof_key_sims = settings_data["out-of-focus-input"]


    def resize_background(self, event):
        if not self.show_bg_image:
            return  # Skip resizing if the background image is not shown

        # Resize the image to fit the window
        width = event.width
        height = event.height

        # Resize the original image to the new size
        self.rezised_image = self.original_image.resize((width, height))

        # Update the PhotoImage
        self.image = ImageTk.PhotoImage(self.rezised_image)
        self.image_label.config(image=self.image)  # Update the label with the new image

    def create_widgets(self, max_columns=3):  # Add max_columns to control buttons per row
        self.buttons = []  # Store button references to access them later

        row = 0  # Start at the first row
        col = 0  # Start at the first column

        # Loop through button_data_list to create multiple buttons
        for button_data in self.button_data_list:
            # Create a button for each entry
            button = ttk.Button(self, style=button_data["style"], text=button_data["name"],
                                command=lambda bd=button_data: self.play_audio(bd))

            # Position the button in the grid
            button.grid(row=row, column=col, padx=5, pady=5, sticky="w")

            self.buttons.append((button, button_data))  # Keep track of button and its data

            # Update column position
            col += 1

            # If the number of columns reaches max_columns, reset column and move to the next row
            if col >= max_columns:
                col = 0  # Reset to the first column
                row += 1  # Move to the next row


    def play_audio(self, button_data):
        audio_manager.play_audio(button_data)

    def handle_keypress(self, event):
        if not self.allow_keypresses: return
        if hasattr(event, "fake"):
            if event.fake and not self.oof_key_sims: return
        pressed_key = event.keysym.upper()  # Convert the pressed key to uppercase
        # Iterate over all buttons to check their keybinds
        for button, button_data in self.buttons:
            keybind = button_data.get("keybind", "").upper()  # Keybind for each button
            if pressed_key == keybind and keybind:  # Match the pressed key with the button's keybind
                button.invoke()  # Simulate a button press
                return "break"
            
    def update_buttons(self):
        for button, _ in self.buttons:
            button.destroy()
        self.create_widgets()
    
    def reload_bg_image(self, forced=False):
        # print(self.image_vis.get())
        self.show_bg_image = bool(self.settings_data["bg-images-shown"])
        if self.show_bg_image or forced:
            if self.settings_data["board-bg-image-path"] != "":
                # Load the original image
                self.original_image = Image.open(self.settings_data["board-bg-image-path"])
            else:
                self.original_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))  # Fully transparent
            self.image = ImageTk.PhotoImage(self.original_image)
            # self.image_label = tk.Label(self.main_area, image=self.image, bg="white")
            self.image_label.config(image=self.image)
            # print("Reloading image - (re)showing")
        else:
            self.original_image = None
            self.image = None
            self.rezised_image = None
            # print("Reloading image - (re)setting image to none")

    def setup_image(self):
        """Load and optionally resize the image to be displayed in the bottom-right corner."""

        if self.settings_data["setup-bg-image-path"] != "":
            # Load the original image
            self.original_image = Image.open(self.settings_data["setup-bg-image-path"])
        else:
            self.original_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))  # Fully transparent

        # Convert the image to a PhotoImage object to display in Tkinter
        self.image = ImageTk.PhotoImage(self.original_image)
        self.image_label = tk.Label(self, image=self.image, bg="white")
        self.reload_bg_image()