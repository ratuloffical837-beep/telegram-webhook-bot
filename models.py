import json
import os

# simple local JSON storage
DB_FILE = "database.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"users": {}, "messages": []}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def save_user(user_id):
    data = load_db()
    data["users"][str(user_id)] = True
    save_db(data)

def save_message(user_id, text):
    data = load_db()
    data["messages"].append({"user": user_id, "text": text})
    save_db(data)
