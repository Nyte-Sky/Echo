import json
import os


root_directory = os.path.join(os.getenv('APPDATA'), 'Echo')
data_file = os.path.join(root_directory, 'button_data.json')
styles_file = os.path.join(root_directory, 'styles.json')
icon_file = os.path.join(root_directory, 'scroll.ico')
ffmpeg_path = os.path.join(root_directory, 'ffmpeg', 'bin', 'ffmpeg.exe')

def check_startup():
    if not os.path.exists(data_file) or False:
        with open(data_file, "w") as file:
            data =  {"buttons": [], 
                    "settings": {
                    "board-bg-image-path": "",
                    "setup-bg-image-path": "",
                    "bg-images-shown": True,
                    "sound-download-path": "",
                    "out-of-focus-input": False
                    }}
            json.dump(data, file, indent=4)
        # file.close()

def load_data():
    if os.path.exists(data_file) and True:
        with open(data_file, 'r') as f:
            return json.load(f)
    else:
        print("Error: Data not found")

def save_data(data):
    # print(f"Saving {data} to {data_file}")
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)
    
def load_styles():
    with open(styles_file, "r") as file:
        styles = json.load(file)
    return styles
