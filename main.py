#internal libraries
import json
import os
import getpass
import re
import time

#project libraries
import commands

# ANSI escape codes for colors
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'

#globals
current_user = {}

def clear(): #clear console
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For macOS and Linux
        _ = os.system('clear')

def login(users):
    clear()
    for i in range(3):
        username = input("Username:")
        password = getpass.getpass("Password:") #getpass.getpass() hides password
        time.sleep(1) #just to make it hard to bruteforcei

        if username in users:
            if users[username]["password"] == password: #will crash if i put both in AND, username will not necessarily exist in users
                print(GREEN + "Welcome to Fitness Center!" + RESET)
                return {"username": username, "user_type": users[username]["user_type"]} #dict (json is also a dict format 
        
        print(RED + "Username does not exist or password is incorrect. Please try again" + RESET)

    print(RED + "You have exceeded three attempts, please run the program again" + RESET)
    exit(0)

def register(user_data):
    clear()
    digits = '0123456789'
    symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'
    while True:
        username = input("Username: ")
        time.sleep(1) #just to make it hard to bruteforce
        if username in user_data["users"]:
            print(RED + "Sorry, this username has been taken" + RESET)
        else:
            break

    print("\nPassword must contain at least one number, one symbol, and 10 characters")
    while True:
        password = getpass.getpass("Password:")
        if len(password) <= 10:
            print(RED + "Password must be more than 10 characters." + RESET)
            continue
        if not any(c in digits for c in password):
            #any() returns true if any x in iterable is True. OR of everything
            print(RED + "Password must contain at least one number." + RESET)
            continue
        if not any(c in symbols for c in password):
            print(RED + "Password must contain at least one symbol." + RESET)
            continue
        break

    email = input("Email: ")

    while not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email): #Check email format with regex 
        print(RED + "Invalid email format. Please try again." + RESET)
        email = input("Email: ")

    user_data["users"][username] = {
        "password": password,
        "email": email,
        "user_type": "Member"
    }

    clear()
    print(f'Username: {username} \nemail: {email}')
    
    confirmed = input("\nRegister? (y/n) ")

    if confirmed == "y":
        with open("userData/accounts.json", "w") as f:
            json.dump(user_data, f, indent=4)
        print(GREEN + "Registered user, please login again" + RESET)
        return
    else:
        clear()
        return


def main():  # This function will be run first
    try:
        with open("userData/accounts.json", "r") as f:
                user_data = json.load(f)
    except FileNotFoundError:
        print(RED + "Error: Can't find accounts.json" + RESET)
        exit(1)
    except json.JSONDecodeError:
        print(RED + "Error: Invalid JSON format in 'accounts.json'." + RESET)
        exit(1)
    except Exception as e:
        print(RED + f'Error: {e}' + RESET)
        exit(1)

    clear()

    key = int(input("1. Login \n2. Register \n3. Exit\n"))
    
    if key == 1: 
        global current_user
        current_user = login(user_data["users"]) #users only because im not modifying accounts.json
        print(GREEN + f'You are now logged in as {current_user["username"]}, permissions: {current_user["user_type"]}' + RESET)
    elif key == 2:
        register(user_data) #the entire thing
    elif key == 3:
        exit(0)


if __name__ == "__main__":
    main()
