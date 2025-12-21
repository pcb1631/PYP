import files
import json
from tui import TUI, timeTUI
import time
from datetime import datetime
from colors import BG_BLUE, BG_GREEN, BG_PURPLE, BG_RED, RED, RESET, BG_MAGENTA, BOLD


from commands import load_accounts, save_accounts

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
        print("\n")

    

current_user = {"username": 'pcb'}

def trainer_frontend(current_user):
    pass

def member_frontend(current_user):
    bookings = load_bookings()
    user_data = load_accounts()
    users = user_data["users"]
    trainers = []

    for user in users:
        if users[user]["user_type"] == "Trainer":
            trainers.append(user)

    while True:
        trainer = TUI(BG_MAGENTA, "Select trainer", trainers, verbose=True)
        if trainer is None:
            return

        if trainer not in bookings or not bookings[trainer]:
            print(f"{RED}Trainer {trainer} does not have any slots.{RESET}")
            time.sleep(1)
            continue
        
        while True:
            slots = []
            for slot in bookings[trainer]:
                
                bookedBy = bookings[trainer][slot]["bookedBy"]
                start = epoch_to_readable(bookings[trainer][slot]["start"])
                end = epoch_to_readable(bookings[trainer][slot]["end"])

                string = f"{slot} | {start} => {end}"
                
                if bookedBy is None:
                    string += f"{RESET} {BG_GREEN}(Available){RESET}"
                
                if bookedBy is not None:
                    string += f"{RESET} {BG_RED}(Booked){RESET}"

                if bookedBy == current_user["username"]:
                    string += f"{RESET} {BG_BLUE}(Booked by you){RESET}"
                
                slots.append(string)
            
            slots.insert(0, "Back")
            selection = TUI(BG_PURPLE, f"Slots for {trainer}", slots, verbose=False)

            if selection == 0: # back
                break
            selection -= 1 # offset for back
            selection = str(selection)

            bookedBy = bookings[trainer][selection]["bookedBy"]
            if bookedBy is not None:
                if bookedBy == current_user["username"]:
                    print(RED + "Remove booking? (y/n)" + RESET)
                    if input() == "y":
                        bookings[trainer][selection]["bookedBy"] = None
                        save_bookings(bookings)
                    continue
            
            print(f"Book slot {selection}? (y/n)")
            if input() == "y":
                bookings[trainer][selection]["bookedBy"] = current_user["username"]
                save_bookings(bookings)
            else:
                continue        

member_frontend(current_user)