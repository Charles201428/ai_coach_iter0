# memory.py
import json
import os

MEMORY_FILE = "user_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memory = json.load(f)
    else:
        memory = {}
    return memory

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)

def get_user_memory(user_email):
    memory = load_memory()
    return memory.get(user_email, [])

def add_to_user_memory(user_email, conversation_entry):
    memory = load_memory()
    if user_email not in memory:
        memory[user_email] = []
    memory[user_email].append(conversation_entry)
    save_memory(memory)
