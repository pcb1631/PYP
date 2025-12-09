import getpass
import json
import datetime
import os
import uuid
import shutil
import difflib
from tui import TUI
from colors import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, BG_BLACK, BG_RED, BG_GREEN, BG_YELLOW, BG_BLUE, BG_MAGENTA, BG_CYAN, BG_WHITE, BOLD, RESET
import files
import kb

# this file (commands.py) will contain some abstraction, and the functions provided for commands in command mode

def clear():                    # clear console
    if os.name == 'nt':         # For Windows
        _ = os.system('cls')
    else:                       # For macOS and Linux
        _ = os.system('clear')  # _ means idgaf about the return value
    

def load_json_file(filepath):       # generic json loader
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
    
def save_json_file(filepath, data): # generic json saver
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(RED + f"Error saving to {filepath}: {e}" + RESET)
        return False

def load_accounts():                # returns None with errors
    try:
        with open(files.ACCOUNTS_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(RED + "Error: Can't find accounts.json" + RESET)
        return None
    except json.JSONDecodeError:
        print(RED + "Error: Invalid JSON format in 'accounts.json'." + RESET)
        return None
    except Exception as e:
        print(RED + f'Error: {e}' + RESET)
        return None

def save_accounts(user_data):       # returns False with errors
    try:
        with open(files.ACCOUNTS_PATH, "w") as f:
            json.dump(user_data, f, indent=4)
        return True
    except Exception as e:
        print(RED + f"Error saving accounts: {e}" + RESET)
        return False

# TODO: Select user via uuid for admin functions 



#The following functions will actually be commands, the first argument should always be current_user for logging

#THE FIRST ARGUMENT IS ALWAYS current_user
def admin_delete_account(current_user, delete_user=None): #delete_user is optional argument
    user_data = load_accounts()
    if user_data is None:
        return

    if delete_user is None:
        delete_user = input("Enter username to delete: ")

    if delete_user not in user_data["users"]:
        print("User not found")
        return

    confirmed = input(f'\n Delete user "{delete_user}"? (y/n): ')

    if confirmed.lower() == 'y':
        del user_data["users"][delete_user]    
    else:
        return
    
    # Save updated data
    if not save_accounts(user_data):
        return

    # Log the deletion
    timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    log_entry = f"\n{timestamp} ACCOUNT: {delete_user} DELETED BY: {current_user["username"]}\n"
    try:
        with open(files.ACCOUNTS_LOG_PATH, "a") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(RED + f"Error logging: {e}" + RESET)

    print(GREEN + f"Account '{delete_user}' deleted successfully." + RESET)

def admin_add_account(current_user):
    user_data = load_accounts()
    if user_data is None:
        return

    while True:
        username = input("New user username: ")
        if username in user_data["users"]:
            print("User already exists")
        else:
            break

    email = input("Email: ")
    password = getpass.getpass("Password: ")
    usertype = input("User type (Must be verbatim of user type in accounts.json): ")

    print(f'\nUsername: {username}\nEmail: {email}\nUser type: {usertype}')
    confirmed = input('\nAdd new user? (y/n): ')

    if confirmed.lower() == 'y':
        user_data["users"][username] = {
            "password": password,
            "email": email,
            "user_type": usertype,
            "uuid": str(uuid.uuid4())
        }
    else:
        return

    if not save_accounts(user_data):
        return

    # Log the account creation
    timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    log_entry = f"\n{timestamp} ACCOUNT: {username} CREATED BY: {current_user['username']}"
    try:
        with open(files.ACCOUNTS_LOG_PATH, "a") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(RED + f"Error logging: {e}" + RESET)

    print(GREEN + f"Account '{username}' created successfully." + RESET)

def admin_edit_account(current_user, username=None):
    user_data = load_accounts()
    if user_data is None:
        return
    
    if username is None:
        username = input("User to edit: ")

    if username not in user_data["users"]:
        print("User does not exist")
        return
    
    print(f"\nUsername: {username}")
    print(f"Email: {user_data['users'][username]['email']}")
    print(f"User type: {user_data['users'][username]['user_type']}")
    print(f"password: {'*' * len(user_data['users'][username]['password'])}")


    new_username = input("New username (leave blank to keep current): ")
    if new_username == username:
        print(RED + "lol" + RESET)
        return
    if new_username == "":
        new_username = username

    new_email = input("New email: ")
    if new_email == "":
        new_email = user_data["users"][username]["email"]
    
    new_usertype = input("New user type: ")
    if new_usertype == "":
        new_usertype = user_data["users"][username]["user_type"]
    
    new_password = getpass.getpass("New password: ")
    if new_password == "":
        new_password = user_data["users"][username]["password"]


    print(f'\nUsername: {new_username or username}\nEmail: {new_email}\nUser type: {new_usertype}')
    confirmed = input('\nSave changes? (y/n): ')

    if confirmed.lower() == 'y':
        uuid = user_data["users"][username]["uuid"]
        del user_data["users"][username]
        user_data["users"][new_username] = {
            "password": new_password,
            "email": new_email,
            "user_type": new_usertype,
            "uuid": uuid
        }
    else:
        return
    
    
    # Log the update
    timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    log_entry = f"\n{timestamp} ACCOUNT: {username} UPDATED BY: {current_user['username']} TO: {new_username}\n"
    try:
        with open(files.ACCOUNTS_LOG_PATH, "a") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(RED + f"Error logging: {e}" + RESET)


    if not save_accounts(user_data):
        return
    print(GREEN + f"Account '{new_username}' updated successfully." + RESET)

def admin_view_account(current_user, username=None):
    user_data = load_accounts()
    if user_data is None:
        return
    
    if username is None:
        username = input("User to view: ")
    
    if username not in user_data["users"]:
        print("User does not exist")
        return
    
    pw = input("Show password? (y/n): ")
    if pw.lower() == "y":
        pw = user_data["users"][username]["password"]
    else:
        pw = "*" * len(user_data["users"][username]["password"])

    print(f"\nUsername: {username}")
    print(f"Email: {user_data['users'][username]['email']}")
    print(f"User type: {user_data['users'][username]['user_type']}")
    print(f"password: {pw}")
    print(f'UUID: {user_data["users"][username]["uuid"]}')

def admin_ban_account(current_user, username=None):
    user_data = load_accounts()
    if user_data is None:
        return
    
    users = list(user_data["users"].keys())

    if username is None:
        username = TUI(MAGENTA + BOLD, "Select user to ban", users,True)
    
    if username is None:    #User pressed CTRL+C
        return
    
    try:
        with open(files.BANNED_PATH, "r") as banned_file:
            banned_users = banned_file.read().splitlines()
    except Exception as e:
        print(RED + f"Error reading {files.BANNED_PATH}: {e}" + RESET)
        return
    
    if username in banned_users:
        print(RED + "User is already banned" + RESET)
        return
    
    confirmed = input(f'\n Ban user "{username}"? (y/n): ')

    if confirmed.lower() == 'y':
        try:
            with open(files.BANNED_PATH, "a") as banned_file:
                banned_file.write(username + "\n")
        except Exception as e:
            print(RED + f"Error saving to {files.BANNED_PATH}: {e}" + RESET)

        #log the ban 
        timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        log_entry = f"\n{timestamp} ACCOUNT: {username} BANNED BY: {current_user['username']}\n"
        try:
            with open(files.ACCOUNTS_LOG_PATH, "a") as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(RED + f"Error logging: {e}" + RESET)

    print(GREEN + f"Account '{username}' banned successfully." + RESET)

def admin_unban_account(current_user, username=None):
    user_data = load_accounts()
    if user_data is None:
        return
    
    users = list(user_data["users"].keys())

    if username is None:
        username = TUI(MAGENTA + BOLD, "Select user to unban", users,True)
    
    if username is None:    #User pressed CTRL+C
        return
    
    confirmed = input(f'\n Unban user "{username}"? (y/n): ')
    
    if confirmed.lower() == 'y':
        try:
            with open(files.BANNED_PATH, "r+") as banned_file:
                banned_file.seek(0)
                banned_file.truncate()
                banned_file.write("\n".join([line for line in banned_file if line.strip() != username]))
        except Exception as e:
            print(RED + f"Error saving to {files.BANNED_PATH}: {e}" + RESET)

        #log the unban
        timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        log_entry = f"\n{timestamp} ACCOUNT: {username} UNBANNED BY: {current_user['username']}\n"
        try:
            with open(files.ACCOUNTS_LOG_PATH, "a") as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(RED + f"Error logging: {e}" + RESET)

    print(GREEN + f"Account '{username}' unbanned successfully." + RESET)

def direct_messages(current_user, username=None): # dont touch this yet 
    user_data = load_accounts()
    if user_data == None:
        return

    users = list(user_data["users"].keys())

    if username is None:
        username = TUI(BG_MAGENTA + BOLD, "Pick someone to talk to", users, True)



def checkin(current_user, username=None):
    user_data = load_accounts()
    if user_data == None:
        return

    if username == None:
        username = input("Check in member: ")

    if username not in user_data["users"]:
        print("User does not exist")
        return

    if user_data["users"][username]["user_type"] != "Member":
        print("User is not a member")
        return

    confirmed = input(f'\n Check in user "{username}"? (y/n): ')

    if confirmed.lower() == 'y':
        timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        log_entry = f"\n{timestamp} MEMBER: {username} CHECKED IN BY: {current_user['username']}\n"
        try:
            with open(files.CHECKIN_LOG_PATH, "a") as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(RED + f"Error logging: {e}" + RESET)

        print(GREEN + f"Member '{username}' checked in successfully." + RESET)
    else:
        return
    
def member_manage_profile(current_user):
    user_data = load_accounts()
    if user_data is None:
        return



# Read booking.json
def load_bookings(filename=files.BOOKING_PATH):
    with open(filename, "r") as booking_file:
        return json.load(booking_file)

# Save bookings into json file
def save_bookings(data, filename=files.BOOKING_PATH):
    with open(filename, "w") as booking_file:
        json.dump(data, booking_file, indent=4)

# Displays trainer list
def display_trainer_list(bookings):
    print("Available Trainers:")
    for i, trainer in enumerate(bookings.keys(), start=1):
        print(f"{i}. {trainer}")

# Let's user choose trainer
def trainer_selection(bookings):
    display_trainer_list(bookings)
    choice = int(input("Enter trainer number of your choice: "))
    if choice != [1, 2, 3, 4, 5]:
        print("Invalid input. Try again.")
        trainer_selection(bookings)
    else:
        trainer_key = list(bookings.keys())[choice - 1]
        return trainer_key

# Display time slots of trainers
def display_slots(bookings, trainer_key):
    print(f"\nTime slots for {trainer_key}:")
    trainer_slots = bookings[trainer_key]
    for slot_id, slot in trainer_slots.items():
        status = "Available" if slot["booked_by"] is None else f"Booked by {slot['booked_by']}"
        print(f"{slot_id}: {slot['start']} - {slot['end']} ({status})")

# Booking time slot for trainers
def booking_slots(bookings, trainer_key, member_name):
    display_slots(bookings, trainer_key)
    slot_choice = input("Enter slot number to book a slot: ")

    slot = bookings[trainer_key][slot_choice]
    if slot != [1, 2, 3, 4, 5, 6]:
        print("Invalid slot number")
        booking_slots(bookings, trainer_key, member_name)
    else:
        if slot["booked_by"] is None:
            slot["booked_by"] = member_name
            print("Booking successful!")
            save_bookings(bookings)  # save to json file
        else:
            print("This slot has already been booked")

# View booking function for members
def view_member_bookings(bookings, member_name):
    print(f"\n{member_name}'s bookings:")
    found = False
    for trainer_key, trainer_slots in bookings.items():  # Loop through trainers
        for slot_id, slot in trainer_slots.items():      # Loop through slots
            if slot["booked_by"] == member_name:
                print(f"- Trainer: {trainer_key}, Slot {slot_id}: {slot['start']} - {slot['end']}")
                found = True

    if not found:
        print("No bookings found.")

def member_booking_menu(current_user):
    bookings = load_bookings()
    member_name = current_user["username"]
    trainer_key = trainer_selection(bookings)
    booking_slots(bookings, trainer_key, member_name)



def send_comment(current_user): # For members to send comments or feedback to specific trainers
    try:
        with open(files.ACCOUNTS_PATH, "r") as f:
            user_data = json.load(f)

        #Displays a list of all trainers in the JSON file
        trainers = []

        for username in user_data["users"]:
            if user_data["users"][username].get("user_type") == "Trainer":
                trainers.append(username)

        if not trainers:
            print("No trainers found in the system.")
            return

        # User will now choose which trainer to send a message to
        verbose = True
        trainer_choice = TUI(BG_MAGENTA + BOLD, "Which trainer would you like to send a message to?\n", trainers, verbose)

        if trainer_choice is None:
            return

        # User will now type their message
        message = input("Please enter your message: ").strip()

        if not message:
            print(RED + "Comment cannot be empty." + RESET)
            return

        #The message will now be saved in 'messages.log' in the format: current_user|trainer name|message
        try:
            with open(files.COMMENTS_LOG_PATH, "a") as message_file:
                message_file.write(
                    f"{current_user['username']}|{trainer_choice}|{message}\n"
                )
        except FileNotFoundError:
            print(RED + "Error: comments.log file not found." + RESET)
        except Exception as e:
            print(RED + f"An unexpected error occurred: {e}" + RESET)

        print(GREEN + "\nYour message has been successfully sent." + RESET)

    except FileNotFoundError:
        print(RED + "Error: account.json file not found." + RESET)

    except json.decoder.JSONDecodeError:
        print(RED + "Error: accounts.json file has been corrupted" + RESET)

    except Exception as e:
        print(RED + f"An unexpected error occurred: {e}" + RESET)

# For trainers to view messages that have been sent to them
def view_comments(current_user):
    # noinspection SpellCheckingInspection
    delim = "|"
    try:
        inbox = []
        with open(files.COMMENTS_LOG_PATH, "r", encoding="utf-8") as f: #Reads the messages.log file
            for raw in f:
                line = raw.strip()
                if not line:
                    continue

                parts = line.split(delim, 2) #Split each line into 3 parts, with "|" being the seperator
                if len(parts) < 3:
                    continue

                member_username, trainer_username, message = parts #Assign each individual part from the variable "part" their own variables
                if current_user['username'] == trainer_username: # Check if the current trainer matches the recipient of the message (Was the message sent to you?))
                    inbox.append((member_username, message))

        if not inbox:
            print(f"You have not received any messages.")
            return

        print(f"\nComments:")
        for idx, (member, msg) in enumerate(inbox, start=1):
            print(f"{idx}. From {member}: {msg}")

    except FileNotFoundError:
        print("comments.log file not found.")
    #print("Invalid slot selected.")
    return None

def viewlogs(current_user, logfile=None):
    options=[files.ACCOUNTS_LOG_PATH, files.CHECKIN_LOG_PATH, files.BANNED_PATH]


    if logfile is None:
        while True:
            logfile=TUI(BG_RED, "Choose log file", options, verbose=True)
            
            if logfile is None: # if user presses CTRL+C
                break

            with open(logfile, "r") as f:
                content = f.read().splitlines()
                _ = TUI(BG_RED, "", content, verbose=False)

    else:
        with open(logfile, "r") as f:
            content = f.read().splitlines()
            _ = TUI(BG_RED, "", content, verbose=False)



