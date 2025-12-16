import files
import json
from tui import TUI
import datetime
from colors import RED, RESET

def epoch_to_readable(ms_timestamp):
    """Convert milliseconds since epoch to DDMMYY HHMM format.
    
    Args:
        ms_timestamp: Milliseconds since epoch
        
    Returns:
        str: Formatted datetime string in DDMMYY HHMM format
    """
    dt = datetime.datetime.fromtimestamp(ms_timestamp / 1000)
    return dt.strftime("%d/%m/%y %H:%M")

def load_bookings(filename=files.BOOKING_PATH):
    with open(filename, "r") as booking_file:
        return json.load(booking_file)

def save_bookings(data, filename=files.BOOKING_PATH):
    with open(filename, "w") as booking_file:
        json.dump(data, booking_file, indent=4)

def generate_next_7_days(current_user): # generates 7 days ahead, with 4 slots in each day
    bookings = load_bookings()
    save_bookings(bookings)

def trainer_view(current_user):
    bookings = load_bookings()
    trainer = current_user["username"]
    slots = bookings[trainer]

    for slot in slots:
        print(f"slot {slot}:")

        start = epoch_to_readable(slots[slot]["start"])
        end = epoch_to_readable(slots[slot]["end"])
        bookedBy = slots[slot]["bookedBy"]

        print(f"start: {start}")
        print(f"end: {end}")
        print(f"bookedBy: {bookedBy}")
        print("\n")

current_user = {"username": "trainer_user"}
trainer_view(current_user)

    