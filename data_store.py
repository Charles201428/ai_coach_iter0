# data_store.py
import json
import os

DATA_FILE = "user_data.json"

def load_user_history(username):
    """
    Load the conversation history for a given username.
    Returns a list of conversation turns.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        return data.get(username, [])
    else:
        return []

def save_user_history(username, history):
    """
    Save the conversation history for a given username.
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}
        
    data[username] = history
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
