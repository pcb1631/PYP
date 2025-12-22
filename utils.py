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