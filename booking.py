# Read booking.json
def load_bookings(filename=files.BOOKING_PATH):
    with open(filename, "r") as booking_file:
        return json.load(booking_file)

# Save bookings into json file
def save_bookings(data, filename=files.BOOKING_PATH):
    with open(filename, "w") as booking_file:
        json.dump(data, booking_file, indent=4)

#automatically generates slots
def auto_generate_slots(bookings):
    time_slots = [
        ("10:00", "12:00"),
        ("12:00", "14:00"),
        ("14:00", "16:00"),
        ("16:00", "18:00"),
        ("18:00", "20:00"),
        ("20:00", "22:00")
    ]

    days = generate_next_7_days()

    for trainer_key in bookings.keys():
        for date in days:
            for i, (start, end) in enumerate(time_slots, start=1):
                slot_id = f"{date}_{i}"

                #Only create slot if missing
                if slot_id not in bookings[trainer_key]:
                    bookings[trainer_key][slot_id] = {
                        "date": date,
                        "start": start,
                        "end": end,
                        "booked_by": None
                    }

    save_bookings(bookings)


# Displays trainer list
def display_trainer_list(bookings):
    print("Available Trainers:")
    for i, trainer in enumerate(bookings.keys(), start=1):
        print(f"{i}. {trainer}")

# Let's user choose trainer
def trainer_selection(bookings):
    display_trainer_list(bookings)
    choice = int(input("Enter trainer number of your choice: "))
    if choice < 1 or choice > len(bookings):
        print("Invalid input. Try again.")
        return trainer_selection(bookings)
    else:
        trainer_key = list(bookings.keys())[choice - 1]
        return trainer_key


def generate_next_7_days():
    today = datetime.now().date()
    days = []
    for i in range(7):
        d = today + timedelta(days=i)
        days.append(d.strftime("%Y-%m-%d"))
    return days


def date_selection():
    days = generate_next_7_days()
    print("\nChoose a date:")
    for i, d in enumerate(days, start=1):
        print(f"{i}. {d}")
    choice = int(input("Enter date of your choice: "))
    if choice < 1 or choice > len(days):
        print("Invalid input. Try again.")
        return date_selection()
    else:
        return days[choice - 1]

# Display time slots of trainers
def display_time_slots(bookings, trainer_key, date):
    print(f"\nTime slots for {trainer_key} on {date}:")
    trainer_slots = bookings[trainer_key]

    available_slots = {}

    for slot_id, slot in trainer_slots.items():
        if slot["date"] == date:
            status = "Available" if slot["booked_by"] is None else f"Booked by {slot['booked_by']}"
            print(f"{slot_id}: {slot['start']} - {slot['end']} ({status})")
            available_slots[slot_id] = slot

# Booking time slot for trainers
def booking_slots(bookings, trainer_key, member_name):
    date = date_selection()

    available_slots = display_time_slots(bookings, trainer_key, date)

    if not available_slots:
        print("\nNo available slots available for this date.")
        return

    slot_choice = input("Enter slot number to book a slot: ")

    if slot_choice not in available_slots:
        print("Invalid input. Try again.")
        return booking_slots(bookings, trainer_key, member_name)

    slot = available_slots[slot_choice]

    if slot["booked_by"] is None:
        slot["booked_by"] = member_name
        print("Booking successful!")
        save_bookings(bookings)
    else:
        print("This slot has already been booked.")

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