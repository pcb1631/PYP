#internal libraries
import os
import getpass
import re
import time

#local project libraries
import commands

#ANSI escape codes for text colors
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
        time.sleep(1) #just to make it hard to bruteforce

        if username in users:
            if users[username]["password"] == password: #will crash if I put both in AND
                print(GREEN + "Welcome to Fitness Center!" + RESET)
                return {"username": username, "user_type": users[username]["user_type"]}
        
        print(RED + "Username does not exist or password is incorrect. Please try again" + RESET)
        


        
        # Log failed login attempt
        import datetime
        timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
        log_entry = f"\n{timestamp} FAILED LOGIN ATTEMPT: {username}"
        try:
            with open("logs/accounts.log", "a") as log_file:
                log_file.write(log_entry)
        except Exception as e:
            print(RED + f"Error logging: {e}" + RESET)

    print(RED + "You have exceeded three attempts, please run the program again" + RESET)
    exit(0)

def register(user_data):
    clear()

    while True:
        username = input("Username: ")
        time.sleep(1) #just to make it hard to bruteforce

        if username in user_data["users"]:
            print(RED + "Sorry, this username has been taken" + RESET)
        else:
            print(GREEN + "Username available" + RESET)
            break
    
    time.sleep(0.1) #small delay for UX
    print("\nPassword must contain at least one number, one symbol, and 10 characters")
    while True:
        password = getpass.getpass("Password: ")

        if len(password) <= 10:
            print(RED + "Password must be more than 10 characters." + RESET)
            continue
        
        if not any(c.isdigit() for c in password): #any() returns true if any x in iterable is True. OR of everything
            print(RED + "Password must contain at least one number." + RESET)
            continue

        if not any(not c.isalnum() for c in password):
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

    if confirmed.lower() == "y":
        if commands.save_accounts(user_data): #returns False with errors
            print(GREEN + "Registered user, please login again" + RESET)
            time.sleep(2)
        return
    else:
        return

def command_mode():
    #   Will now act like a shell with commands
    #   Commands are categorized by permissions, examples:
    #   msa admin_delete_account
    #   msa admin_add_account 
    #   mma delete_account 
    #   etc.
    #   Users are only allowed to run commands, if the permission of the command is in the permissions list

    #I think after we're done with everything, I'll build something like a TUI when the user just types a permission
    user_data = commands.load_accounts()
    if user_data is None:
        exit(1)
    
    permissions = user_data["permissions"].get(current_user["user_type"], [])
    if "A" in permissions:
        permissions = ["msa", "mma"] #Admin has all permissions, make sure to add every permission here

    #we're not gonna write a bunch of if else like noobs
    cmdlist = {}
    cmdlist["msa"] = {
        "admin_delete_account": commands.admin_delete_account,
        "admin_add_account": commands.admin_add_account
    }
    cmdlist["mma"] = {}

    print("\nType 'h' or 'help' for list of commands within your permission level, 'exit' or CTRL+C to logout and quit.")
    print(f"Your permissions: {', '.join(permissions)}")

    try: #Wrapping the whole thing to catch keyboard interrupts
        while True:
            command = input()
            if command == "exit":
                print("Bye!")
                exit(0)
                
            elif command == "h" or command == "help":
                for p in permissions:
                    print(f"{p}: {', '.join(cmdlist[p].keys())}") #prints keys only 

            else:
                command = command.split()
                
                if len(command) < 2:
                    print(RED + "TUI coming soon" + RESET)
                    continue
                
                perm = command[0]
                cmd_name = command[1]
                args = command[2:] if len(command) > 2 else []
                
                if perm not in permissions:
                    print(RED + "Unknown permission / Access denied" + RESET)
                    continue
                if cmd_name not in cmdlist[perm]:
                    print(RED + "Unknown command" + RESET)
                    continue
                
                # Call the function stored in the dictionary
                func = cmdlist[perm][cmd_name]
                try: 
                    func(current_user, *args)
                except Exception as e:
                    print(RED + f"Error executing command: {e}" + RESET)

    except KeyboardInterrupt:
        print("\nBye!")
        exit(0)


def main():  # This function will be run first 
    user_data = commands.load_accounts() #returns None with errors
    if user_data is None:
        exit(1)
    
    while True:
        clear()
        key = int(input("1. Login \n2. Register \n3. Exit\n"))

        if key == 1: 
            global current_user
            current_user = login(user_data["users"]) #users only, because im not modifying accounts.json
            print(GREEN + f'You are now logged in as {current_user["username"]}, permissions: {current_user["user_type"]}' + RESET)
            command_mode()
        elif key == 2:
            register(user_data) #the entire thing
        elif key == 3:
            exit(0)
        else:
            print(RED + "Invalid input" + RESET)


if __name__ == "__main__":
    main()
