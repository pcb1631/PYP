import files
import json
from tui import TUI
from datetime import datetime
from colors import RED, RESET, BG_MAGENTA, BOLD

def epoch_to_readable(ms_timestamp):
    dt = datetime.fromtimestamp(ms_timestamp / 1000)
    return dt.strftime("%d/%m/%y %H:%M")

def load_bookings(filename=files.BOOKING_PATH):
    with open(filename, "r") as booking_file:
        return json.load(booking_file)

def save_bookings(data, filename=files.BOOKING_PATH):
    with open(filename, "w") as booking_file:
        json.dump(data, booking_file, indent=4)

def generate_next_7_days(current_user): # generates 7 days ahead, with 4 slots in each day
    bookings = load_bookings()
    trainer = current_user["username"]
    


    save_bookings(bookings)

def add_slots(current_user, year=datetime.now().year, month=1, day=1, hour=0, minute=0):
    bookings = load_bookings()
    trainer = current_user["username"]
    start = int(datetime(year, month, day, hour, minute).timestamp() * 1000)
    end = start + 60 * 60 * 1000
    


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
add_slots(current_user)

    