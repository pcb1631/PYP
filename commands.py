from enum import CONTINUOUS
import getpass
import json
import os
import uuid
import time

from tui import TUI
from colors import *
import files
import kb
from utils import *
# this file (commands.py) will contain some abstraction, and the functions provided for commands in command mode

def clear():                    # clear console
    if os.name == 'nt':         # For Windows
        _ = os.system('cls')
    else:                       # For macOS and Linux
        _ = os.system('clear')  # _ means idgaf about the return value

# TODO: Select user via uuid for admin functions



#The following functions will actually be commands, the first argument should always be current_user for logging

#THE FIRST ARGUMENT IS ALWAYS current_user
def admin_delete_account(current_user, delete_user=None): #delete_user is optional argument
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    users = list(user_data["users"])

    if delete_user is None:
        delete_user = TUI(BG_RED, "Select user to delete", users, verbose=True)

    if delete_user not in users:
        print("User not found")
        return

    confirmed = input(f'\n Delete user "{delete_user}"? (y/n): ')

    if confirmed.lower() == 'y':
        del user_data["users"][delete_user]
    else:
        return

    if find(delete_user, files.ONLINE_PATH): # if user is online, add to delete list
        write_line(delete_user, files.DELETE_PATH)

    if save_json(files.ACCOUNTS_PATH, user_data, current_user):
        print(GREEN + f"Account '{delete_user}' deleted successfully." + RESET)
    else:
        print(RED + f"Failed to delete account '{delete_user}'." + RESET)
        return

    timestamp = epoch_to_readable(time.time())
    log_entry = f"\n{timestamp} ACCOUNT: {delete_user} DELETED BY: {current_user['username']}\n"
    if not write_line(log_entry, files.ACCOUNTS_LOG_PATH):
        return

def admin_add_account(current_user):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    while True:
        username = input("New user username: ")
        if username in user_data["users"]:
            print("User already exists")
        else:
            break

    email =         input("Email: ")
    password =      getpass.getpass("Password: ")
    usertype =      input("User type (Must be verbatim of user type in accounts.json): ")
    age =           int(input("Age: "))
    gender =        input("Gender (m/f): ")
    phone_number =  input("Phone number: ")

    print("Username: " + username)
    print("Email: " + email)
    print("User type: " + usertype)
    print("Age: " + str(age))
    print("Gender: " + gender)
    print("Phone number: " + phone_number)
    confirmed = input('\nAdd new user? (y/n): ')

    if confirmed.lower() == 'y':
        user_data["users"][username] = {
            "password": password,
            "email": email,
            "age": age,
            "gender": gender,
            "phone number": phone_number,
            "user_type": usertype,
            "uuid": str(uuid.uuid4()),
            "balance - RM": 0
        }
    else:
        return

    if usertype == "Trainer":
        booking_data = load_json(files.BOOKING_PATH)

        booking_data[username] = {} # code will break if trainer doesnt exist in booking.json

        if not save_json(files.BOOKING_PATH, booking_data, current_user):
            return

    if not save_json(files.ACCOUNTS_PATH, user_data, current_user):
        return

    # Log the account creation
    timestamp = epoch_to_readable(time.time())
    log_entry = f"\n{timestamp} ACCOUNT: {username} CREATED BY: {current_user['username']}"
    if not write_line(log_entry, files.ACCOUNTS_LOG_PATH):
        return

    print(GREEN + f"Account '{username}' created successfully." + RESET)

def admin_edit_account(current_user, username=None):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    if username is None:
        username = TUI(BG_RED, "Select user to edit", list(user_data["users"].keys()), verbose=True)

    if username not in user_data["users"]:
        print("User does not exist")
        return

    keys = user_data["users"][username].keys()

    print("\nCurrent user details:")
    for key in keys:
        if key == "password":
            print(f"password: {'*' * len(user_data['users'][username]['password'])}")
        else:
            print(f"{key}: {user_data['users'][username][key]}")

    new_username = input("New username (leave blank to keep current): ")
    if new_username == "":
        new_username = username
    else:
        if new_username in user_data["users"]:
            print("Username already exists")
            return
        user_data["users"][new_username] = user_data["users"][username]
        del user_data["users"][username]

    for key in keys:
        if key == "uuid":
            continue
        if key == "password":
            new_password = getpass.getpass("New password: ")
            if new_password == "":
                continue
            else:
                user_data["users"][new_username][key] = new_password
                continue
        new_value = input(f"New {key}: ")
        if new_value == "":
            continue
        else:
            user_data["users"][new_username][key] = new_value

    confirm = input("\nConfirm changes? (y/n): ")
    if confirm.lower() != "y":
        return

    if not save_json(files.ACCOUNTS_PATH, user_data, current_user):
        return
    # Log the update
    timestamp = epoch_to_readable(time.time())
    log_entry = f"\n{timestamp} ACCOUNT: {username} UPDATED BY: {current_user['username']} TO: {new_username}\n"
    if not write_line(log_entry, files.ACCOUNTS_LOG_PATH):
        return


    print(GREEN + f"Account '{new_username}' updated successfully." + RESET)

    if user_data["users"][new_username]["user_type"] == "Trainer":
        booking_data = load_json(files.BOOKING_PATH)
        booking_data[new_username] = {}
        if not save_json(files.BOOKING_PATH, booking_data, current_user):
            print(RED + "Failed to add" + new_username + "to booking.json" + RESET)

def fd_delete_account(current_user, delete_user=None):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    users = user_data["users"]

    members = []
    for user in users:
        if users[user]["user_type"] == "Member":
            members.append(user)

    if delete_user is None:
        delete_user = TUI(BG_RED, "Select member to delete", members, verbose=True)

    if delete_user is None:
        return

    if users[delete_user]["user_type"] != "Member":
        print(RED + delete_user +" is not a Member." + RESET)
        return

    if delete_user not in users:
        print("User not found")
        return

    confirmed = input(f'\n Delete user "{delete_user}"? (y/n): ')

    if confirmed.lower() == 'y':
        del user_data["users"][delete_user]
    else:
        return

    if find(delete_user, files.ONLINE_PATH): # if user is online, add to delete list
        write_line(delete_user, files.DELETE_PATH)

    if save_json(files.ACCOUNTS_PATH, user_data, current_user):
        print(GREEN + f"Account '{delete_user}' deleted successfully." + RESET)
    else:
        print(RED + f"Failed to delete account '{delete_user}'." + RESET)
        return

    timestamp = epoch_to_readable(time.time())
    log_entry = f"\n{timestamp} ACCOUNT: {delete_user} DELETED BY: {current_user['username']}\n"
    if not write_line(log_entry, files.ACCOUNTS_LOG_PATH):
        return

def fd_add_account(current_user):
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    if username in user_data["users"]:
        print(RED + f"Username '{username}' already exists." + RESET)
        return

    user_data["users"][username] = {
        "username": username,
        "password": password,
        "uuid": str(uuid.uuid4()),
        "user_type": "Member",
        "email": None,
        "phone number": None,
        "age": 0,
        "gender": None,
        "balance - RM": 0.0,
        "membership_tier": None,
    }

    if save_json(files.ACCOUNTS_PATH, user_data, current_user):
        print(GREEN + f"Member '{username}' added successfully." + RESET)
    else:
        print(RED + f"Failed to add account '{username}'." + RESET)
        return

    timestamp = epoch_to_readable(time.time())
    log_entry = f"{timestamp} ACCOUNT: {username} ADDED BY: {current_user['username']}"
    if not write_line(log_entry, files.ACCOUNTS_LOG_PATH):
        return

def fd_edit_account(current_user, username=None):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    members = []
    for user in user_data["users"]:
        if user_data["users"][user]["user_type"] == "Member":
            members.append(user)

    if username is None:
        username = TUI(BG_RED, "Select user to edit", members, verbose=True)

    if username not in user_data["users"]:
        print("User does not exist")
        return
    
    if user_data["users"][username]["user_type"] != "Member":
        print(RED + "Only members can be edited." + RESET)
        return
    
    keys = user_data["users"][username].keys()

    print("\nCurrent user details:")
    for key in keys:
        if key == "password":
            print(f"password: {'*' * len(user_data['users'][username]['password'])}")
        else:
            print(f"{key}: {user_data['users'][username][key]}")

    new_username = input("New username (leave blank to keep current): ")
    if new_username == "":
        new_username = username
    else:
        if new_username in user_data["users"]:
            print("Username already exists")
            return
        user_data["users"][new_username] = user_data["users"][username]
        del user_data["users"][username]

    for key in keys:
        if key == "uuid":
            continue
        if key == "password":
            new_password = getpass.getpass("New password: ")
            if new_password == "":
                continue
            else:
                user_data["users"][new_username][key] = new_password
                continue
        if key == "user_type":
            continue
        
        new_value = input(f"New {key}: ")
        if new_value == "":
            continue
        else:
            user_data["users"][new_username][key] = new_value

    confirm = input("\nConfirm changes? (y/n): ")
    if confirm.lower() != "y":
        return

    if not save_json(files.ACCOUNTS_PATH, user_data, current_user):
        return
    # Log the update
    timestamp = epoch_to_readable(time.time())
    log_entry = f"\n{timestamp} ACCOUNT: {username} UPDATED BY: {current_user['username']} TO: {new_username}\n"
    if not write_line(log_entry, files.ACCOUNTS_LOG_PATH):
        return


    print(GREEN + f"Account '{new_username}' updated successfully." + RESET)

def user_edit_account(current_user):
    username = current_user["username"]
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    keys = user_data["users"][username].keys()
    for key in keys:
        if key == "password" or key == "uuid":
            continue
        print(f"{key}: {user_data['users'][username][key]}")

    password = user_data["users"][username]["password"]
    print(f"Password: {'*' * len(password)}")

    for key in keys:
        if key != "password" and key != "uuid" and key != "user_type":
            newkey = input(f"New {key}: ")
            if newkey != "":
                user_data["users"][username][key] = newkey

    new_password = getpass.getpass("New password: ")
    if new_password != "":
        user_data["users"][username]["password"] = new_password

    print("\nNew user details:")
    for key in keys:
        if key == "password" or key == "uuid":
            continue
        print(f"{key}: {user_data['users'][username][key]}")

    pw = user_data['users'][username]['password']
    print("Password: " + "*" * len(pw))


    confirm = input("\nConfirm changes? (y/n): ")
    if confirm.lower() != "y":
        return
    else:
        if not save_json(files.ACCOUNTS_PATH, user_data, current_user):
            return
        print(GREEN + f"Account '{username}' updated successfully." + RESET)

    timestamp = epoch_to_readable(time.time())
    log_entry = f"\n{timestamp} ACCOUNT: {username} UPDATED BY: {current_user['username']}\n"
    if not write_line(log_entry, files.ACCOUNTS_LOG_PATH):
        return


def admin_view_account(current_user, username=None):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    if username is None:
        username = TUI(BG_RED, "Select user to view", list(user_data["users"].keys()), verbose=True)

    if username not in user_data["users"]:
        print("User does not exist")
        return

    pw = input("Show password? (y/n): ")
    if pw.lower() == "y":
        pw = user_data["users"][username]["password"]
    else:
        pw = "*" * len(user_data["users"][username]["password"])

    print(f"\nUsername: {username}")
    keys = user_data["users"][username].keys()
    for key in keys:
        if key == "password":
            print(f"password: {pw}")
        else:
            print(f"{key}: {user_data['users'][username][key]}")

def user_view_account(current_user):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    username = current_user["username"]

    pw = input("Show password? (y/n): ")
    if pw.lower() == "y":
        pw = user_data["users"][username]["password"]
    else:
        pw = "*" * len(user_data["users"][username]["password"])

    print(f"\nUsername: {username}")
    keys = user_data["users"][username].keys()
    for key in keys:
        if key == "password":
            print(f"password: {pw}")
        else:
            print(f"{key}: {user_data['users'][username][key]}")

def admin_ban_account(current_user, username=None):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    users = list(user_data["users"].keys())

    if username is None:
        username = TUI(BG_PURPLE + BOLD, RED + "Select user to ban" + RESET, users,True)

    if username not in users:
        print(RED + "User not found" + RESET)
        return

    if username is None:    #User pressed CTRL+C
        return

    if find(username, files.BANNED_PATH):
        print(RED + "User is already banned" + RESET)
        return

    confirmed = input(f'\n Ban user "{username}"? (y/n): ')

    if confirmed.lower() == 'y':
        if not write_line(username, files.BANNED_PATH):
            return

        #log the ban
        timestamp = epoch_to_readable(time.time())
        log_entry = f"{timestamp} ACCOUNT: {username} BANNED BY: {current_user['username']}"
        if not write_line(log_entry, files.ACCOUNTS_LOG_PATH):
            return

        print(GREEN + f"Account '{username}' banned successfully." + RESET)

def admin_unban_account(current_user, username=None):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    users = list(user_data["users"].keys())

    if username is None:
        username = TUI(MAGENTA + BOLD, "Select user to unban", users,True)

    if username is None:    #User pressed CTRL+C in TUI
        return

    confirmed = input(f'\n Unban user "{username}"? (y/n): ')

    if confirmed.lower() == 'y':
        try:
            with open(files.BANNED_PATH, "r") as f:
                banned_users = f.read().splitlines()
            with open(files.BANNED_PATH, "w") as f:
                for user in banned_users:
                    if user != username:
                        f.write(user)
        except Exception as e:
            print(RED + f"Error saving to {files.BANNED_PATH}: {e}" + RESET)

        #log the unban
        timestamp = epoch_to_readable(time.time())
        log_entry = f"{timestamp} ACCOUNT: {username} UNBANNED BY: {current_user['username']}"
        if not write_line(log_entry, files.ACCOUNTS_LOG_PATH):
            return

        print(GREEN + f"Account '{username}' unbanned successfully." + RESET)

def direct_messages(current_user, username=None): # dont touch this yet
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data == None:
        return

    users = list(user_data["users"].keys())

    if username is None:
        username = TUI(BG_MAGENTA + BOLD, "Pick someone to talk to", users, True)

def send_comment(current_user): # For members to send comments or feedback to specific trainers
    timedate = epoch_to_readable(time.time()) # Get the current date and time

    timedate = list(timedate)
    timedate[8] = '|'
    timedate = ''.join(timedate)
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

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

    if not write_line(f"{timedate}|{current_user['username']}|{trainer_choice}|{message}", files.COMMENTS_LOG_PATH):
        return

    print(GREEN + "\nYour message has been successfully sent." + RESET)



# For trainers to view messages that have been sent to them
def view_comments(current_user):
    # noinspection SpellCheckingInspection
    delim = "|"
    try:
        inbox = []
        with open(files.COMMENTS_LOG_PATH, "r", encoding="utf-8") as f: #Reads the comments.log file
            for raw in f:
                line = raw.strip()
                if not line:
                    continue

                parts = line.split(delim, 4) #Split each line into 5 parts, with "|" being the seperator
                if len(parts) < 5:
                    continue

                date, time, member_username, trainer_username, message = parts #Assign each individual part from the variable "part" their own variables
                if current_user['username'] == trainer_username: # Check if the current trainer matches the recipient of the message (Was the message sent to you?))
                    inbox.append((date, time, member_username, message))

        if not inbox:
            print(f"You have not received any messages.")
            return

        print(f"\nComments:")
        for idx, (date, time, member, msg) in enumerate(inbox, start=1):
            print(f"{idx}.[{date} {time}] From {member}: {msg}")

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

            parse = []

            if logfile[-4:] == ".log":
                for line in content:
                    line = line.split(" ")
                    if line[0] == '#' or line[0] == "":
                        continue

                    parse.append(f"{BLUE}{line[0]}{RESET} {GREEN}{line[1]}{RESET} {' '.join(line[2:])}")
                content = parse

                _ = TUI(BG_RED, f"{BG_MAGENTA}{logfile}{RESET}", content, verbose=False)

    else:
        with open(logfile, "r") as f:
            content = f.read().splitlines()
            _ = TUI(BG_RED, f"{BG_MAGENTA}{logfile}{RESET}", content, verbose=False)

