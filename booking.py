import files
import json
from tui import TUI
from datetime import datetime, timedelta
from colors import RED, RESET

def load_bookings(filename=files.BOOKING_PATH):
    with open(filename, "r") as booking_file:
        return json.load(booking_file)

def save_bookings(data, filename=files.BOOKING_PATH):
    with open(filename, "w") as booking_file:
        json.dump(data, booking_file, indent=4)

def generate_next_7_days(current_user): # generates 7 days ahead, with 4 slots in each day
    bookings = load_bookings()
    save_bookings(bookings)



    