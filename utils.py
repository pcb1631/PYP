import files
import json
from colors import *
from datetime import datetime

def conflict(trainer, time):
    bookings = load_json(files.BOOKING_PATH)
    if trainer not in bookings:
        raise KeyError(f"Trainer '{trainer}' not found in bookings")
    
    slots = bookings[trainer]
    for slot in slots:
        if time >= slots[slot]["start"] and time <= slots[slot]["end"]:
            return slot
        else: 
            return None

def epoch_to_readable(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%d/%m/%y %H:%M")

def find(username, filepath):
    """
    Does username exist in this file?
    
    :param str username:        The username
    :param str filepath:        File path
    :return:                    does the username exists in the file
    :rtype:                     bool
    :raises FileNotFoundError:  if the file doesn't exist
    """
    try:
        with open(filepath, "r") as f:
            data = f.read().splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filepath}' not found")
    except Exception as e:
        raise Exception(f"Error reading from {filepath}: {e}")
    return username in data

def write_line(line, filepath):
    try:
        with open(filepath, "a") as f:
            f.write("\n" + line)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filepath}' not found")
    except Exception as e:
        raise Exception(f"Error writing to {filepath}: {e}")


def load_json(filepath):       # generic json loader
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{filepath}' not found")
    except json.JSONDecodeError:
        raise Exception(f"Invalid JSON format in '{filepath}'")
    except Exception as e:
        raise Exception(f"Error loading from {filepath}: {e}")
    
def save_json(filepath, data, current_user): # generic json saver
    username = current_user["username"]
    
    if find(username, files.BANNED_PATH):
        raise PermissionError("You are banned")
    if find(username, files.DELETE_PATH):
        raise PermissionError("Your account has been deleted")
    
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise Exception(f"Error saving to {filepath}: {e}")
