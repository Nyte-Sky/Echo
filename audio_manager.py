import pygame
from tkinter import messagebox

def initialize_audio():
    pygame.mixer.init()
    pygame.mixer.set_num_channels(16)

def play_audio(button_data, volume=None):
    global playing_music, playing_sounds
    if volume: button_data["volume"] = volume
    # Play audio specific to the button
    if "sound_path" in button_data and button_data["sound_path"]:
        if button_data["type"] == "short":
            play_short_audio(button_data["sound_path"], button_data["volume"])
        elif button_data["type"] == "long":
            play_continuous_audio(button_data["sound_path"], button_data["volume"])
        elif button_data["type"] == "repeat":
            play_looped_audio(button_data["sound_path"], button_data["volume"])
        elif button_data["type"] == "music":
            play_music(button_data["sound_path"], button_data["volume"])

def play_short_audio(sound_path, volume):
    global playing_music, playing_sounds
    if sound_path:
        try:
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(volume ** 2)
            pygame.mixer.Sound.play(sound)
        except pygame.error:
            messagebox.showerror("Error", "Could not play the selected audio file.")
    else:
        messagebox.showinfo("No Audio", "No audio file specified for this button.")

playing_sounds = {}

def stop_continuous_audio(sound_path):
    global playing_music, playing_sounds
    if sound_path in playing_sounds.keys():
        sound = playing_sounds[sound_path]
        if pygame.mixer.Sound.get_num_channels(sound) != 0:
            pygame.mixer.Sound.stop(sound)
            playing_sounds.pop(sound_path)
    elif playing_music["path"] == sound_path:
        sound: pygame.mixer.Sound = playing_music["sound"]
        sound.stop()
        playing_music = {"path": None, "sound": None, "filled": False}

def play_continuous_audio(sound_path, volume):
    global playing_music, playing_sounds
    if sound_path:
            try:
                if not sound_path in playing_sounds.keys():
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(volume ** 2)
                    pygame.mixer.Sound.play(sound)
                    playing_sounds[sound_path] = sound
                else:
                    sound = playing_sounds[sound_path]
                    if pygame.mixer.Sound.get_num_channels(sound) != 0:
                        pygame.mixer.Sound.stop(sound)
                        playing_sounds.pop(sound_path)
                    else:
                        playing_sounds.pop(sound_path)
                        sound = pygame.mixer.Sound(sound_path)
                        sound.set_volume(volume ** 2)
                        pygame.mixer.Sound.play(sound)
                        playing_sounds[sound_path] = sound
            except pygame.error:
                messagebox.showerror("Error", "Could not play the selected audio file.")
    else:
        messagebox.showinfo("No Audio", "No audio file specified for this button.")
    
def play_looped_audio(sound_path, volume):
    global playing_music, playing_sounds
    if sound_path:
            try:
                if not sound_path in playing_sounds.keys():
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(volume ** 2)
                    pygame.mixer.Sound.play(sound, loops=-1)
                    playing_sounds[sound_path] = sound
                else:
                    sound = playing_sounds[sound_path]
                    if pygame.mixer.Sound.get_num_channels(sound) != 0:
                        pygame.mixer.Sound.stop(sound)
                        playing_sounds.pop(sound_path)
                    else:
                        playing_sounds.pop(sound_path)
                        sound = pygame.mixer.Sound(sound_path)
                        sound.set_volume(volume ** 2)
                        pygame.mixer.Sound.play(sound, loops=-1)
                        playing_sounds[sound_path] = sound
            except pygame.error:
                messagebox.showerror("Error", "Could not play the selected audio file.")
    else:
        messagebox.showinfo("No Audio", "No audio file specified for this button.")
    
playing_music = {"path": None, "sound": None, "filled": False}

def play_music(sound_path, volume):
    global playing_music, playing_sounds
    try:
        sound = pygame.mixer.Sound(sound_path)
        sound.set_volume(volume ** 2)
        if not (playing_music["filled"]):
            playing_music["path"] = sound_path
            playing_music["sound"] = sound
            playing_music["filled"] = True
            pygame.mixer.Sound.play(sound, loops=-1)
        elif playing_music["path"] == sound_path:
            currently_playing: pygame.mixer.Sound = playing_music["sound"]
            currently_playing.fadeout(2000)
            playing_music = {"path": None, "sound": None, "filled": False}
        else:
            currently_playing: pygame.mixer.Sound = playing_music["sound"]
            currently_playing.fadeout(2000)
            playing_music["path"] = sound_path
            playing_music["sound"] = sound
            sound.play(loops=-1, fade_ms=2000)
    except pygame.error:
        messagebox.showerror("Error", "Could not play the selected audio file.")