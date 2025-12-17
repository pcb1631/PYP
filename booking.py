import files
import json
from tui import TUI, timeTUI
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
    
    start = timeTUI(prompt="start", ms_timestamp=start)
    if start is None:
        return
    end = timeTUI(prompt="end", ms_timestamp=end)
    if end is None:
        return

    slots = bookings[trainer].keys()
    max_slot = max([int(slot) for slot in slots]) if slots else 0
    bookings[trainer][max_slot + 1] = {"start": start, "end": end, "bookedBy": None}
    save_bookings(bookings)
    
def delete_slot(current_user, slot=None):
    trainer = current_user["username"]
    bookings = load_bookings()
    slots = bookings[trainer]
    
    if slot is None:
        slot = input("Slot to delete: ")

    slot = str(slot)
    del bookings[trainer][slot]
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

def trainer_frontend(current_user):
    pass

    