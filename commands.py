import getpass
import json
import datetime
import os
import uuid
import shutil
import difflib
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
        username = TUI(MAGENTA + BOLD, "Select user to ban", users,True)
    
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
        timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        log_entry = f"\n{timestamp} ACCOUNT: {username} BANNED BY: {current_user['username']}\n"
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
        timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        log_entry = f"\n{timestamp} ACCOUNT: {username} UNBANNED BY: {current_user['username']}\n"
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

def transaction_history(current_user):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    if current_user:

        print("\n--- Transaction History ---")
        print(f"Username: {current_user['username']}")
        print("Membership tier:", user_data["users"][current_user["username"]]["membership_tier"])
        with open("transactions.json", 'r') as f:
            transactions = json.load(f)
        print("Amount:", transactions["transaction"][current_user["username"]]["amount"])
        print("Timestamp:", transactions["transaction"][current_user["username"]]["timestamp"])


    else:
        print("No transaction to view.")

def membership_renewal(current_user):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    now = datetime.datetime.now()

    if current_user:
        with open("transactions.json", 'r') as f:
            transactions = json.load(f)

        timestamp_str = transactions["transaction"][current_user["username"]]["timestamp"]
        last_transaction_time = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

        days_since = (now - last_transaction_time).days

        if days_since >=30:
            print("Your current membership tier:", user_data["users"][current_user["username"]]["membership_tier"])
            with open("transactions.json", 'r') as f:
                transactions = json.load(f)
            print("Amount:", transactions["transaction"][current_user["username"]]["amount"])
            rn = input("Renew membership? (y/n): ")
            if rn == 'y':
                with open("transactions.json", 'r') as f:
                    transactions = json.load(f)
                    amount = transactions["transaction"][current_user["username"]]["amount"]
                rnpm = input(YELLOW + f"RM{amount} will be charged. Pay now? (y/n): " + RESET)
                if rnpm == 'y':
                    print(GREEN + "Membership renew successfully." + RESET)
                    cost = transactions["transaction"][current_user["username"]]["amount"]
                    if "balance - RM" not in user_data["users"][current_user["username"]]:
                        print(RED + "Insufficient balance. Please top up first." + RESET)

                    if user_data["users"][current_user["username"]]["balance - RM"] < cost:
                        print(RED + "Insufficient balance. Please top up first." + RESET)
                    else:
                        user_data["users"][current_user["username"]]["balance - RM"] -= cost
                        with open(files.ACCOUNTS_PATH, "w") as f:
                            json.dump(user_data, f, indent=4)
                        print(
                            GREEN + f"Membership has been renewed successfully. Your current balance: RM{user_data["users"][current_user["username"]]["balance - RM"]}." + RESET)

                else:
                    print(RED + "Payment cancelled" + RESET)

            else:
                print(RED + "Cancelled." + RESET)
                return

        else:
            print(RED + "You have not reach the expiry date" + RESET)
            return

def update_age(current_user):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    if "Age" in user_data["users"][current_user["username"]]:
        ua = input("Update age? (y/n):")
        if ua == "y":
            uaa = int(input(YELLOW + "Insert your age:" + RESET))
            user_data["users"][current_user["username"]]["Age"] = uaa
            with open(files.ACCOUNTS_PATH, "w") as f:
                  json.dump(user_data, f, indent=4)
            print(GREEN + f"Age {uaa} updated successfully." + RESET)

        else:
            print(RED + "Age update cancelled." + RESET)
    else:
        age = input("You have not add your age. Add age? (y/n):")
        if age == "y":
            age = int(input(YELLOW + "Insert your age:" + RESET))
            user_data["users"][current_user["username"]]["Age"] = age
            with open(files.ACCOUNTS_PATH, "w") as f:
                json.dump(user_data, f, indent=4)
            print(GREEN + f"Age {age} updated successfully." + RESET)
        else:
            print(RED + "Age update cancelled." + RESET)

def update_phone_number(current_user):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    if "Phone Number" in user_data["users"][current_user["username"]]:
        upn = input("Update Phone Number? (y/n):")
        if upn == "y":
            upn = int(input(YELLOW + "Insert your new Phone Number:" + RESET))
            user_data["users"][current_user["username"]]["Phone Number"] = upn
            with open(files.ACCOUNTS_PATH, "w") as f:
                json.dump(user_data, f, indent=4)
            print(GREEN + f"Phone number {upn} updated successfully." + RESET)

        else:
            print(RED + "Phone Number update cancelled." + RESET)
    else:
        pn = input("You have not add your Phone Number. Add Phone Number? (y/n):")
        if pn == "y":
            pn = int(input(YELLOW + "Insert your Phone Number:" + RESET))
            user_data["users"][current_user["username"]]["Phone Number"] = pn
            with open(files.ACCOUNTS_PATH, "w") as f:
                json.dump(user_data, f, indent=4)
            print(GREEN + f"Phone Number {pn} updated successfully." + RESET)
        else:
            print(RED + "Phone number update cancelled." + RESET)

def standard_membership(current_user):
    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        return

    if "membership_tier" not in user_data["users"][current_user["username"]]:
        user_data["users"][current_user["username"]]["membership_tier"] = "None"
        with open(files.ACCOUNTS_PATH, "w") as f:
            json.dump(user_data, f, indent=4)

    standard_cost = 150

    if user_data["users"][current_user["username"]]["membership_tier"] == "Standard":
        print(RED + "You had a membership" + RESET)
        return

    elif user_data["users"][current_user["username"]]["membership_tier"] == "Premium":
        print(RED + "You had a membership" + RESET)
        return

    elif user_data["users"][current_user["username"]]["membership_tier"] == "Student":
        print(RED + "You had a membership" + RESET)
        return

    else:
        print(YELLOW + "30 days Standard membership - RM150" + RESET)
        pp = input("Proceed payment? (y/n): ")

        if pp == "y":
            if "balance - RM" not in user_data["users"][current_user["username"]]:
                print(RED + "Insufficient balance. Please top up first." + RESET)

            if user_data["users"][current_user["username"]]["balance - RM"] < standard_cost:
                print(RED + "Insufficient balance. Please top up first." + RESET)

            else:
                user_data["users"][current_user["username"]]["balance - RM"] -= standard_cost
                user_data["users"][current_user["username"]]["membership_tier"] = "Standard"
                with open(files.ACCOUNTS_PATH, "w") as f:
                    json.dump(user_data, f, indent=4)
                print(
                    GREEN + f"Thank you for purchasing our membership. Your current balance: RM{user_data["users"][current_user["username"]]["balance - RM"]}." + RESET)

                with open("transactions.json",'r') as f:
                    transactions = json.load(f)

                if "transaction" not in transactions:
                    transactions["transaction"] = {}

                transactions["transaction"][current_user["username"]]={
                                "membership_tier": "Standard",
                                "amount": standard_cost,
                                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }

                with open("transactions.json", "w") as f:
                    json.dump(transactions, f, indent=4)

        else:
            print(RED + "Payment cancelled" + RESET)
            return

def premium_membership(current_user):
    user_data = load_accounts()
    if user_data is None:
        return

    if "membership_tier" not in user_data["users"][current_user["username"]]:
        user_data["users"][current_user["username"]]["membership_tier"] = "None"
        with open(files.ACCOUNTS_PATH, "w") as f:
            json.dump(user_data, f, indent=4)

    premium_cost = 250

    if user_data["users"][current_user["username"]]["membership_tier"] == "Standard":
        print(RED + "You had a membership" + RESET)
        return

    elif user_data["users"][current_user["username"]]["membership_tier"] == "Premium":
        print(RED + "You had a membership" + RESET)
        return

    elif user_data["users"][current_user["username"]]["membership_tier"] == "Student":
        print(RED + "You had a membership" + RESET)
        return

    else:
        print(YELLOW + "30 days Premium membership - RM250" + RESET)
        pp = input("Proceed payment? (y/n): ")

        if pp == "y":
            if "balance - RM" not in user_data["users"][current_user["username"]]:
                print(RED + "Insufficient balance. Please top up first." + RESET)

            if user_data["users"][current_user["username"]]["balance - RM"] < premium_cost:
                print(RED + "Insufficient balance. Please top up first." + RESET)

            else:
                user_data["users"][current_user["username"]]["balance - RM"] -= premium_cost
                user_data["users"][current_user["username"]]["membership_tier"] = "Premium"
                with open(files.ACCOUNTS_PATH, "w") as f:
                    json.dump(user_data, f, indent=4)
                print(
                    GREEN + f"Thank you for purchasing our membership. Your current balance: RM{user_data["users"][current_user["username"]]["balance - RM"]}." + RESET)

                with open("transactions.json",'r') as f:
                    transactions = json.load(f)

                if "transaction" not in transactions:
                    transactions["transaction"] = {}

                transactions["transaction"][current_user["username"]]={
                                "membership_tier": "Premium",
                                "amount": premium_cost,
                                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }

                with open("transactions.json", "w") as f:
                    json.dump(transactions, f, indent=4)

        else:
            print(RED + "Payment cancelled" + RESET)
            return

def student_membership(current_user):
    user_data = load_accounts()
    if user_data is None:
        return

    if "membership_tier" not in user_data["users"][current_user["username"]]:
        user_data["users"][current_user["username"]]["membership_tier"] = "None"
        with open(files.ACCOUNTS_PATH, "w") as f:
            json.dump(user_data, f, indent=4)

    student_cost = 90

    if user_data["users"][current_user["username"]]["membership_tier"] == "Standard":
        print(RED + "You had a membership" + RESET)
        return

    elif user_data["users"][current_user["username"]]["membership_tier"] == "Premium":
        print(RED + "You had a membership" + RESET)
        return

    elif user_data["users"][current_user["username"]]["membership_tier"] == "Student":
        print(RED + "You had a membership" + RESET)
        return

    else:
        print(YELLOW + "30 days Student membership - RM90" + RESET)
        pp = input("Proceed payment? (y/n): ")

        if pp == "y":
            if "balance - RM" not in user_data["users"][current_user["username"]]:
                print(RED + "Insufficient balance. Please top up first." + RESET)

            if user_data["users"][current_user["username"]]["balance - RM"] < student_cost:
                print(RED + "Insufficient balance. Please top up first." + RESET)

            else:
                user_data["users"][current_user["username"]]["balance - RM"] -= student_cost
                user_data["users"][current_user["username"]]["membership_tier"] = "Student"
                with open(files.ACCOUNTS_PATH, "w") as f:
                    json.dump(user_data, f, indent=4)
                print(
                    GREEN + f"Thank you for purchasing our membership. Your current balance: RM{user_data["users"][current_user["username"]]["balance - RM"]}." + RESET)

            with open("transactions.json", 'r') as f:
                transactions = json.load(f)

            if "transaction" not in transactions:
                transactions["transaction"] = {}

            transactions["transaction"][current_user["username"]] = {
                "membership_tier": "Stundent",
                "amount": student_cost,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            with open("transactions.json", "w") as f:
                json.dump(transactions, f, indent=4)

        else:
            print(RED + "Payment cancelled" + RESET)
            return

def upgrade_membership(current_user):
    user_data = load_accounts()
    if user_data is None:
        return

    standard_upgrade_cost = 100
    student_upgrade_cost = 160

    if "membership_tier" not in user_data["users"][current_user["username"]]:
        print(RED + "You do not have a membership" + RESET)
        return

    if user_data["users"][current_user["username"]]["membership_tier"] == "Standard":
        utp = input(BLUE + "Upgrade to Premium? (y/n): " + RESET)

        if utp == "y":
            pp = input(YELLOW + "RM100 will be charged for upgrade. Proceed payment? (y/n):" + RESET)

            if pp == "y":
              print(GREEN + "Membership upgraded. You membership tier is PREMIUM now" + RESET)
              if user_data["users"][current_user["username"]]["balance - RM"] < standard_upgrade_cost:
                  print(RED + "Insufficient balance. Please top up first." + RESET)

              else:
                  user_data["users"][current_user["username"]]["balance - RM"] -= standard_upgrade_cost
                  with open(files.ACCOUNTS_PATH, "w") as f:
                      json.dump(user_data, f, indent=4)

              if user_data["users"][current_user["username"]]["user_type"] == "Member":
                  user_data["users"][current_user["username"]]["membership_tier"] = "Premium"

              with open(files.ACCOUNTS_PATH, "w") as f:
                  json.dump(user_data, f, indent=4)

            else:
              print(RED + "Payment cancelled" + RESET)

        else:
            print(RED + "Membership tier maintained as Standard" + RESET)

    elif user_data["users"][current_user["username"]]["membership_tier"] == "Student":
        utp = input(BLUE + "Upgrade to Premium? (y/n): " + RESET)

        if utp == "y":
            pp = input(YELLOW + "RM160 will be charged for upgrade. Proceed payment? (y/n):" + RESET)

            if pp == "y":
              print(GREEN + "Membership upgraded. You membership tier is PREMIUM now" + RESET)
              if user_data["users"][current_user["username"]]["balance - RM"] < student_upgrade_cost:
                  print(RED + "Insufficient balance. Please top up first." + RESET)

              else:
                  user_data["users"][current_user["username"]]["balance - RM"] -= student_upgrade_cost
                  with open(files.ACCOUNTS_PATH, "w") as f:
                      json.dump(user_data, f, indent=4)

              if user_data["users"][current_user["username"]]["user_type"] == "Member":
                  user_data["users"][current_user["username"]]["membership_tier"] = "Premium"

              with open(files.ACCOUNTS_PATH, "w") as f:
                  json.dump(user_data, f, indent=4)

            else:
              print(RED + "Payment cancelled" + RESET)

        else:
            print(RED + "Membership tier maintained as Student" + RESET)

    elif user_data["users"][current_user["username"]]["membership_tier"] == "Premium":
        print(RED + "You are already upgraded to Premium." + RESET)

def cancel_membership(current_user):
    user_data = load_accounts()
    if user_data is None:
        return
    if "membership_tier" in user_data["users"][current_user["username"]]:
        cm = input("Cancel membership? (y/n): ")
        if cm == "y":
            print(GREEN + "Membership cancelled." + RESET)
            del user_data["users"][current_user["username"]]["membership_tier"]
            with open(files.ACCOUNTS_PATH, "w") as f:
                json.dump(user_data, f, indent=4)
        else:
            print(RED + "You did not cancel membership" + RESET)
    else:
        print(RED + "You do not have a membership" + RESET)

def top_up_balance(current_user):
    user_data = load_accounts()
    if user_data is None:
        return
    if "balance - RM" not in user_data["users"][current_user["username"]]:
        user_data["users"][current_user["username"]]["balance - RM"] = 0

    try:
        amount = float(input("Enter top up amount (RM):"))
        if amount < 0:
            print(RED + "Invalid amount. Please enter a positive amount." + RESET)
            return

        user_data["users"][current_user["username"]]["balance - RM"] += amount

        with open(files.ACCOUNTS_PATH, "w") as f:
            json.dump(user_data, f, indent=4)
        print(GREEN + f"Top up successful. New balance: RM{user_data["users"][current_user["username"]]["balance - RM"]}." + RESET)

    except ValueError:
        print(RED + "Invalid input. Please enter a number." + RESET)

def notifications(current_user):
    user_data = load_accounts()
    if user_data is None:
        return

    if "membership_tier" not in user_data["users"][current_user["username"]]:
        print("No notification.")

    else:
        with open("transactions.json", 'r') as f:
            transactions = json.load(f)
        print(transactions["transaction"][current_user["username"]]["timestamp"])
        print(GREEN + "Congrats you purchased our membership!" + RESET)


def send_comment(current_user): # For members to send comments or feedback to specific trainers
    timedate = datetime.datetime.now() # Get the current date and time
    date = timedate.strftime("%d/%m/%Y")
    time = timedate.strftime("%H:%M:%S")
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
                    f"{date}|{time}|{current_user['username']}|{trainer_choice}|{message}\n"
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
            print(f"{idx}.[{date}|{time}] From {member}: {msg}")

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

def test ():
    print(current_user)