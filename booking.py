import files
import json
from tui import TUI
from datetime import datetime, timedelta

# Read booking.json
def load_bookings(filename=files.BOOKING_PATH):
    with open(filename, "r") as booking_file:
        return json.load(booking_file)

# Save bookings into json file
def save_bookings(data, filename=files.BOOKING_PATH):
    with open(filename, "w") as booking_file:
        json.dump(data, booking_file, indent=4)

def generate_next_7_days(trainer): # generates 7 days ahead, with 4 slots in each day
    with open(files.BOOKING_PATH, "r") as booking_file:
        bookings = json.load(booking_file)
    
    time_slots = [
        ("10:00", "12:00"),
        ("12:00", "14:00"),
        ("14:00", "16:00"),
        ("16:00", "18:00"),
    ]
    
    today = datetime.now().date()
    # e.g. 2025-12-16

    days = []
    for i in range(7): # 7 days ahead of today 
        d = today + timedelta(days=i)
        days.append(d.strftime("%Y-%m-%d"))

    for day in days: # makes 4 slots in a day. 
        if trainer in bookings and day in bookings[trainer]: # if this particular day exists for this trainer, do not overwrite
            continue
        else:
            for i, (start, end) in enumerate(time_slots, start=1):
                bookings[trainer][day] = {
                    "start": start,
                    "end": end,
                    "booked_by": None
                }
    save_bookings(bookings)


# View booking function for members
def view_member_bookings(bookings, member_name):
    print(f"\n{member_name}'s bookings:")
    found = False
    for trainer_key, trainer_slots in bookings.items():  # Loop through trainers
        for slot_id, slot in trainer_slots.items():      # Loop through slots
            if slot["booked_by"] == member_name:
                print(f"- Trainer: {trainer_key}, Slot {slot_id}: {slot["date"]} {slot["start"]} - {slot["end"]}")
                found = True

    if not found:
        print("No bookings found.")


def main():
    generate_next_7_days("trainer_1")



if __name__ == "__main__":
    main()