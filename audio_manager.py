import pygame
from tkinter import messagebox

def initialize_audio():
    pygame.mixer.init()

def play_audio(sound_path, volume):
    if sound_path:
        try:
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(volume ** 2)
            pygame.mixer.Sound.play(sound)
        except pygame.error:
            messagebox.showerror("Error", "Could not play the selected audio file.")
    else:
        messagebox.showinfo("No Audio", "No audio file specified for this button.")
