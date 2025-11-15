import getpass
import json
import datetime

# ANSI escape codes for text colors
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

def load_accounts(): #returns None with errors
    try:
        with open("userData/accounts.json", "r") as f:
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

def save_accounts(user_data): #returns False with errors
    try:
        with open("userData/accounts.json", "w") as f:
            json.dump(user_data, f, indent=4)
        return True
    except Exception as e:
        print(RED + f"Error saving accounts: {e}" + RESET)
        return False

def admin_delete_account(current_user):
    user_data = load_accounts()
    if user_data is None:
        return

    delete_user = input("Enter username to delete: ")

    if delete_user not in user_data["users"]:
        print("User not found")
        return

    confirmed = input(f'\n Delete user {delete_user}? (y/n): ')

    if confirmed.lower() == 'y':
        del user_data["users"][delete_user]    
    else:
        return
    
    # Save updated data
    if not save_accounts(user_data):
        return

    # Log the deletion
    timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    log_entry = f"{timestamp} ACCOUNT: {delete_user} DELETED BY: {current_user["username"]}\n"
    try:
        with open("logs/accounts.log", "a") as log_file:
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

    print(f'Username: {username}\nEmail: {email}\nUser type: {usertype}')
    confirmed = input('\nAdd new user? (y/n): ')

    if confirmed.lower() == 'y':
        user_data["users"][username] = {
            "password": password,
            "email": email,
            "user_type": usertype
        }
    else:
        return

    if not save_accounts(user_data):
        return

    # Log the account creation
    timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    log_entry = f"{timestamp} ACCOUNT: {username} CREATED BY: {current_user["username"]}\n"
    try:
        with open("logs/accounts.log", "a") as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print(RED + f"Error logging: {e}" + RESET)

    print(GREEN + f"Account '{username}' created successfully." + RESET)
