import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json_manager
import download_audio
import os

class SoundImporter(ttk.Frame):
    def __init__(self, parent, data, settings_data):
        super().__init__(parent)
        self.data = data
        self.settings_data = settings_data
        self.download_path = settings_data["sound-download-path"]

        main_area, top_bar, bottom_bar = self.create_fund_widgets()


        self.create_other_widgets()
        self.create_main_widgets()    
    
    def create_main_widgets(self):
        self.download_widgets = {}

        self.download_widgets["path_label"] = tk.Label(self.main_area, bg="#f5f5f5", bd=1, relief="sunken",
                              text=f"Download to folder: {self.download_path}" if self.download_path != "" else "Download folder not specified.")
        self.download_widgets["path_label"].pack(pady=(50, 5), padx=50)
        self.download_widgets["change_path"] = tk.Button(self.main_area, text="Change download folder", bd=1, 
                                command=self.change_download_path)
        self.download_widgets["change_path"].pack(pady=5, padx=100)

        self.download_widgets["url_enter"] = PlaceholderEntry(self.main_area, placeholder="Enter YouTube URl: ")
        self.download_widgets["url_enter"].pack(pady=5, padx=100)

        self.download_widgets["download_button"] = tk.Button(self.main_area, command=self.download,  text="Download", bd=1, state="normal" if self.download_path != "" else "disabled") 
        self.download_widgets["download_button"].pack(pady=5, padx=100)

    def change_download_path(self):
        file_path = filedialog.askdirectory()
        if file_path:
            self.settings_data["sound-download-path"] = file_path
            json_manager.save_data(self.data)
            self.download_path = self.settings_data["sound-download-path"]
            self.download_widgets["path_label"].config(text=f"Download to folder: {self.download_path}" if self.download_path != "" else "Download folder not specified.")
            self.download_widgets["download_button"].config(state="normal" if self.download_path != "" else "disabled")


    def download(self):
        url = self.download_widgets["url_enter"].store_url()  # Get the URL from the Entry
        success, error, path = download_audio.download_audio(url, self.download_path)  # Download audio

        if success:
            messagebox.showinfo("Success", f"Downloaded  to {path}")
            
        else:
            messagebox.showerror("Error", f"Could not download file. Error: \n{error}")  # Show error if download fails

    def create_other_widgets(self):
        # Create a Label for the text
        descriptor_label = tk.Label(self.top_bar, text="Download sounds from YouTube", bg="lightgray")
        descriptor_label.pack(side=tk.LEFT)  # Place the text on the left

    def create_fund_widgets(self):
        self.top_bar = tk.Frame(self, height=20, bg="lightgray")
        self.top_bar.pack(side="top", fill="x")

        self.main_area = tk.Frame(self, bg="white", width=500, height=300)
        self.main_area.pack(expand=True, fill="both")

        self.bottom_bar = tk.Frame(self, height=20, bg="lightgray")
        self.bottom_bar.pack(side="bottom", fill="x")

        return self.main_area, self.top_bar, self.bottom_bar
    
class PlaceholderEntry(tk.Frame):
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        
        self.placeholder = placeholder
        
        # Create a frame to hold the entry and button together
        self.entry_frame = tk.Frame(self, bg="white")
        self.entry_frame.pack()

        # Create the entry widget
        self.entry = tk.Entry(self.entry_frame, fg='grey', bg="#f5f5f5", width=30)
        self.entry.insert(0, self.placeholder)  # Set placeholder text
        self.entry.bind("<FocusIn>", self.on_entry_click)
        self.entry.bind("<FocusOut>", self.on_focusout)
        self.entry.pack(side=tk.LEFT)  # Pack entry to the left
        
        # Create a clear button
        self.clear_button = tk.Button(self.entry_frame, text="\u2717", command=self.clear_entry, width=2, height=1, relief="ridge")
        self.clear_button.pack(side=tk.LEFT, padx=(5, 0))  # Pack button to the right of the entry

        self.url = ""  # Variable to store the entered URL

    def on_entry_click(self, event):
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)  # Clear the entry
            self.entry.config(fg='black')  # Change text color to black

    def on_focusout(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, self.placeholder)  # Restore placeholder text
            self.entry.config(fg='grey')  # Change text color to grey

    def clear_entry(self):
        self.entry.delete(0, tk.END)  # Clear the entry
        self.entry.config(fg='grey')  # Reset to placeholder color
        self.entry.insert(0, self.placeholder)  # Restore placeholder text
        self.focus()

    def store_url(self):
        self.url = self.entry.get()  # Get the text from the entry
        if self.url == self.placeholder: self.url = ""
        return self.url

