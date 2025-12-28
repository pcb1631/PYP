import files
import json
from datetime import datetime

def conflict(trainer, time):
    bookings = load_bookings()
    slots = bookings[trainer]
    for slot in slots:
        if time >= slots[slot]["start"] and time <= slots[slot]["end"]:
            return slot
        else: 
            return None

def load_bookings(filename=files.BOOKING_PATH):
    with open(filename, "r") as booking_file:
        return json.load(booking_file)

def save_bookings(data, filename=files.BOOKING_PATH):
    with open(filename, "w") as booking_file:
        json.dump(data, booking_file, indent=4)

def epoch_to_readable(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%d/%m/%y %H:%M")

def find(username, filepath):
    try:
        with open(filepath, "r") as f:
            data = f.read().splitlines()
    except FileNotFoundError:
        print(RED + f"Error: Can't find {filepath}" + RESET)
        return False
    except Exception as e:
        print(RED + f"Error: {e}" + RESET)
        return False
    return username in data

def write_line(line, filepath):
    try:
        with open(filepath, "a") as f:
            f.write(line)
    except Exception as e:
        print(RED + f"Error writing to {filepath}: {e}" + RESET)
        return False
    return True


def load_json(filepath):       # generic json loader
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(RED + f"Error: Can't find {filepath}" + RESET)
        return None
    except json.JSONDecodeError:
        print(RED + f"Error: Invalid JSON format in '{filepath}'." + RESET)
        return None
    except Exception as e:
        print(RED + f'Error: {e}' + RESET)
        return None
    
def save_json(filepath, data, current_user): # generic json saver
    username = current_user["username"]
    
    if find(username, files.BANNED_PATH):
        print(RED + "Error: You are banned" + RESET)
        return False
    if find(username, files.DELETE_PATH):
        print(RED + "Error: Your account has been deleted" + RESET)
        return False
    
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(RED + f"Error saving to {filepath}: {e}" + RESET)
        return False