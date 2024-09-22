import json
import os

data_file = "button_data.json"

def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    else:
        # Default structure with an empty button list
        return {"buttons": []}  # Initialize with an empty list of buttons

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)
