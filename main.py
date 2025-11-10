import json #internal libraries
import os
import getpass
import time

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
        password = getpass.getpass("Password:")
        time.sleep(1) #just to make it hard to bruteforcei

        if username in users:
            if users[username]["password"] == password:
                print("Welcome to Fitness Center!")
                return {"username": username, "user_type": users[username]["user_type"]} #dict (json is also a dict format 
        
        print("Username does not exist or password is incorrect. Please try again")

    print("You have exceeded three attempts, please run the program again")
    exit(0)

def register(user_data):
    clear()
    digits = '0123456789'
    symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?/~`'
    while True:
        username = input("Username: ")
        time.sleep(1) #just to make it hard to bruteforce
        if username in user_data["users"]:
            print("Sorry, this username has been taken")
        else:
            break

    while True:
        password = getpass.getpass("Password:")
        if len(password) <= 10:
            print("Password must be more than 10 characters.")
            continue
        if not any(c in digits for c in password):
            #any() returns true if any x in iterable is True. OR of everything
            print("Password must contain at least one number.")
            continue
        if not any(c in symbols for c in password):
            print("Password must contain at least one symbol.")
            continue
        break

    email = input("Email: ")

    user_data["users"][username] = {
        "password": password,
        "email": email,
        "user_type": "Member"
    }

    print(username)
    print(user_data)

    confirmed = input("\nRegister? (y/n)")

    if confirmed:
        with open("userData/accounts.json", "w") as f:
            json.dump(user_data, f, indent=4)
        print("Welcome to Lifestyle Fitness Center!")
        return
    else:
        clear()
        return


def main():  # This function will be run first
    try:
        with open("userData/accounts.json", "r") as f:
                user_data = json.load(f)
    except FileNotFoundError:
        print("Error: Can't find accounts.json")
        exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in 'accounts.json'.")
        exit(1)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)

    clear()

    key = int(input("1. Login \n2. Register \n3. Exit\n"))
    
    if key == 1: 
        global current_user
        current_user = login(user_data["users"]) #users only because im not modifying accounts.json
    elif key == 2:
        register(user_data) #the entire thing
    elif key == 3:
        exit(0)

    print(f'You are now logged in as {current_user["username"]}, permissions: {current_user["user_type"]}')

if __name__ == "__main__":
    main()
