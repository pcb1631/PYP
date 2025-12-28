import json
from tui import TUI, timeTUI
import time
from datetime import datetime
from utils import *
from colors import *
import files


def sort_slots(trainer):
    bookings = load_json(files.BOOKING_PATH)
    slots = []
    for slot in bookings[trainer]:
        slots.append(bookings[trainer][slot])
    slots.sort(key=lambda x: x["start"]) # sort with regards to start time

    bookings[trainer] = {} # clear slots

    for i in range(len(slots)):
        bookings[trainer][str(i)] = slots[i]
    save_json(files.BOOKING_PATH, bookings, current_user)


def generate_next_7_days(current_user): # generates 7 days ahead, with 4 slots in each day
    bookings = load_json(files.BOOKING_PATH)
    trainer = current_user["username"]
    slots = bookings[trainer]
    
    hours = [8, 10, 14, 16]
    for i in range(7):
        for j in range(4):
            start = int(datetime(datetime.now().year, datetime.now().month, datetime.now().day + i, hours[j], 0).timestamp())
            end = start + 60 * 60
            if conflict(trainer, start) or conflict(trainer, end):
                continue
            add_slots_epoch(current_user, start, end)
    print(GREEN + "Generated time slots for next 7 days" + RESET)

def add_slots(current_user, year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, hour=datetime.now().hour, minute=datetime.now().minute):
    bookings = load_json(files.BOOKING_PATH)
    trainer = current_user["username"]
    start = int(datetime(year, month, day, hour, minute).timestamp())
    end = start + 60 * 60
    
    start = timeTUI(prompt="start", timestamp=start, username=trainer)
    if start is None:
        return
    end = timeTUI(prompt="end", timestamp=end, username=trainer)
    if end is None:
        return

    slots = bookings[trainer].keys()
    max_slot = max([int(slot) for slot in slots]) if slots else 0
    bookings[trainer][max_slot + 1] = {
        "start": start,
        "end": end,
        "bookedBy": None,
        "venue": None
    }
    save_json(files.BOOKING_PATH, bookings, current_user)
    print("Added time slot to bookings")
    sort_slots(trainer)
    
def trainer_editor(current_user):
    bookings = load_json(files.BOOKING_PATH)
    trainer = current_user["username"]

    if trainer not in bookings:
        print(RED + "You have no slots to modify" + RESET)
        return
    slots = bookings[trainer]

    strings = []
    for slot in slots:
        start = epoch_to_readable(slots[slot]["start"])
        end = epoch_to_readable(slots[slot]["end"])
        bookedBy = slots[slot]["bookedBy"]
        venue = slots[slot]["venue"]

        string = f"{slot} | {start} => {end}"

        if venue is None:
            string += f"{RESET} {BG_RED}{DARK_GRAY}(Venue not set){RESET}"
        else:
            string += f"{RESET} {BG_BLUE}{DARK_GRAY}(Venue: {venue}){RESET}"
        
        if bookedBy is None:
            string += f"{RESET} {BG_GREEN}{DARK_GRAY}(Available){RESET}"
        else:
            string += f"{RESET} {BG_BLUE}{DARK_GRAY}(Booked by {bookedBy}){RESET}"

        strings.append(string)

    markings = [0] * len(slots)
    idx = 0
    while True: # this can be optimized later
        options = []
        options.append(BLUE + "Done" + RESET)
        for i in range(len(strings)):
            if markings[i] == 0:
                options.append(strings[i])
            if markings[i] == 1:
                options.append(strings[i] + " " + BG_PURPLE + "Member attended" + RESET)
            if markings[i] == 2:
                options.append(strings[i] + " " + BG_RED + DARK_GRAY + "Marked for deletion" + RESET)
            if markings[i] == 3:
                options.append(strings[i] + " " + BG_GREEN + DARK_GRAY + "Marked for freeing" + RESET)
            

        selection = TUI(BG_PURPLE, "Select slot", options, verbose=False, idx=idx)
        idx = selection
        if selection is None:
            return
        if selection == 0:
            break
        selection -= 1 # offset for back

        markings[selection] = (markings[selection] + 1) % 4 # cycle through 0, 1, 2, 3
    
    confirm = input("Save your changes? (y/n): ")
    if confirm == "y":
        for i in range(len(markings)):
            if markings[i] == 1:
                bookings[trainer][str(i)]["Attended"] = True
            if markings[i] == 2:
                del bookings[trainer][str(i)]
            if markings[i] == 3:
                bookings[trainer][str(i)]["bookedBy"] = None
        save_json(files.BOOKING_PATH, bookings, current_user)
        sort_slots(trainer)
    else:
        return

def add_slots_epoch(current_user, start=int(datetime.now().timestamp()), end=int(datetime.now().timestamp())):
    bookings = load_json(files.BOOKING_PATH)
    trainer = current_user["username"]

    slots = bookings[trainer].keys()
    max_slot = max([int(slot) for slot in slots]) if slots else 0
    bookings[trainer][max_slot + 1] = {
        "start": start,
        "end": end,
        "bookedBy": None,
        "venue": None
    }
    save_json(files.BOOKING_PATH, bookings, current_user)
    sort_slots(trainer)

def attendance(current_user):
    bookings = load_json(files.BOOKING_PATH)
    user_data = load_json(files.ACCOUNTS_PATH)
    users = user_data["users"]
    trainers = []
    for user in users:
        if users[user]["user_type"] == "Trainer":
            trainers.append(user)
    
    trainer = TUI(BG_MAGENTA, "Select trainer", trainers, verbose=True)
    if trainer is None:
        return

    slots = bookings[trainer]

    strings = []
    for slot in slots:
        start = epoch_to_readable(slots[slot]["start"])
        end = epoch_to_readable(slots[slot]["end"])
        bookedBy = slots[slot]["bookedBy"]
        venue = slots[slot]["venue"]

        string = f"{slot} | {start} => {end}"

        if venue is None:
            string += f"{RESET} {BG_RED}{DARK_GRAY}(Venue not set){RESET}"
        else:
            string += f"{RESET} {BG_BLUE}{DARK_GRAY}(Venue: {venue}){RESET}"
        
        if bookedBy is None:
            string += f"{RESET} {BG_GREEN}{DARK_GRAY}(Available){RESET}"
        else:
            string += f"{RESET} {BG_BLUE}{DARK_GRAY}(Booked by {bookedBy}){RESET}"

        strings.append(string)

    markings = [0] * len(slots)
    idx = 0
    while True: # this can be optimized later
        options = []
        options.append(BLUE + "Done" + RESET)
        for i in range(len(strings)):
            if markings[i] == 0:
                options.append(strings[i])
            if markings[i] == 1:
                options.append(strings[i] + " " + BG_PURPLE + "Member attended" + RESET)
        selection = TUI(BG_PURPLE, "Select slot", options, verbose=False, idx=idx)
        idx = selection
        if selection is None:
            return
        if selection == 0:
            break
        selection -= 1 # offset for back

        markings[selection] = (markings[selection] + 1) % 2 # cycle through 0, 1
    
    confirm = input("Save your changes? (y/n): ")
    if confirm == "y":
        for i in range(len(markings)):
            if markings[i] == 1:
                bookings[trainer][str(i)]["Attended"] = True
        save_json(files.BOOKING_PATH, bookings, current_user)
    else:
        return

def venue(current_user):
    bookings = load_json(files.BOOKING_PATH)
    user_data = load_json(files.ACCOUNTS_PATH)
    users = user_data["users"]
    trainers = []
    
    for user in users:
        if users[user]["user_type"] == "Trainer":
            trainers.append(user)
    
    trainer = TUI(BG_MAGENTA, "Select trainer", trainers, verbose=True)
    if trainer is None:
        return
    
    slots = bookings[trainer]
    markings = []
    strings = []
    for slot in slots:
        string = ""
        start = epoch_to_readable(slots[slot]["start"])
        end   = epoch_to_readable(slots[slot]["end"])
        string += f"{slot} | {start} => {end}"
        
        if slots[slot]["venue"] is None:
            string += f"{RESET} {BG_RED}No venue{RESET}"
            markings.append(None)
        else:
            string += f"{RESET} {BG_BLUE}Venue: {slots[slot]["venue"]}{RESET}"
            markings.append(slots[slot]["venue"])

        if slots[slot]["bookedBy"] is None:
            string += f"{RESET} {BG_GREEN}Available{RESET}"
        else:
            string += f"{RESET} {BG_BLUE}Booked by: {slots[slot]["bookedBy"]}{RESET}"

        strings.append(string)

    idx = 0
    while True:
        options = []
        for i in range(len(markings)):
            if markings[i] is None:
                options.append(strings[i])
            else:
                options.append(strings[i] + " " + BG_BLUE + "Venue: " + markings[i] + RESET)
        options.insert(0, RED + "Done" + RESET)
        
        selection = TUI(BG_PURPLE, "Assign venues", options, verbose=False, idx=idx)
        if selection is None:
            return
        if selection == 0:
            break
        idx = selection
        selection -= 1


        try:
            venue = input(f"Enter venue for slot {selection}: ")
            if venue == "":
                venue = None 
            
            markings[selection] = venue
        except KeyboardInterrupt:
            print("\nCancelled")
            continue
    
    confirm = input("Save changes? (y/n): ")
    if confirm == "y":
        for i in range(len(markings)):
            if markings[i] is not None:
                bookings[trainer][str(i)]["venue"] = markings[i]
        save_json(files.BOOKING_PATH, bookings, current_user)
    

def member_frontend(current_user):
    bookings = load_json(files.BOOKING_PATH)
    user_data = load_json(files.ACCOUNTS_PATH)
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
        
        idx = 0
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
                    string += f"{RESET} {BG_BLUE}(Venue: {bookings[trainer][slot]["venue"]})"
                
                slots.append(string)
            
            slots.insert(0, RED + "Back" + RESET)
            selection = TUI(BG_PURPLE, f"Slots for {trainer}", slots, verbose=False, idx=idx)
            idx = selection

            if selection == 0 or selection is None: # back or Ctrl+C
                break
            selection -= 1 # offset for back
            selection = str(selection)

            bookedBy = bookings[trainer][selection]["bookedBy"]
            if bookedBy is not None:
                if bookedBy == current_user["username"]:
                    print(RED + "Free booking? (y/n)" + RESET)
                    if input() == "y":
                        bookings[trainer][selection]["bookedBy"] = None
                        save_json(files.BOOKING_PATH, bookings, current_user)
                    continue
                else:
                    continue
            
            print(f"Book slot {selection}? (y/n)")
            if input() == "y":
                bookings[trainer][selection]["bookedBy"] = current_user["username"]
                save_json(files.BOOKING_PATH, bookings, current_user)
            else:
                continue        
