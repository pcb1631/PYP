import getpass
import json
import datetime
import os
import uuid

from colors import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, BOLD, RESET
import files
import kb

# this file (commands.py) will contain some abstraction, and the functions provided for commands in command mode

def clear():                    # clear console
    if os.name == 'nt':         # For Windows
        _ = os.system('cls')
    else:                       # For macOS and Linux
        _ = os.system('clear')  # _ means idgaf about the return value
                            

def TUI(COLOR, pretext, *args): # color must be a constant from colors.py, *args should be a string array 
    options = args              
    selection = 0               # user's selection 
    buffer = []                 # what to print after every "refresh"

    '''
    TODO:  search options
    
    '''
    
    while True:
        print(pretext)

        for i in range(options.len()):
            if i == selection:
                print(COLOR + options[i] + RESET)
            else:
                print(options[i])

        # get user input
        if os.name == 'nt':
            pass
        else:
            pass


    

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

# Checklist:
# Select user via uuid for admin functions 



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

