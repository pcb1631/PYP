#internal libraries
import os
import getpass
import re
import time
import datetime
import uuid

#local project libraries
import commands
from tui import TUI
from colors import RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, BOLD, BG_BLACK, BG_RED, BG_GREEN, BG_YELLOW, BG_BLUE, BG_MAGENTA, BG_CYAN, BG_WHITE, RESET
import files
import booking
#globals
current_user = {}

cmdlist = {} # This is for commands with arguments.
cmdlist["manage_staff_accounts"] = {
    "delete_account":   commands.admin_delete_account,
    "add_account":      commands.admin_add_account,
    "edit_account":     commands.admin_edit_account,
    "view_account":     commands.admin_view_account
}
cmdlist["manage_member_accounts"] = {
    # Add mma commands, and their respective functions here
}
cmdlist["manage_members"] = {
}

cmdlist["send_comments"] = {
    "comment":  commands.send_comment
}
cmdlist["view_comments"] = {
    "view":     commands.view_comments
}
cmdlist["admin"] = {
    "ban":      commands.admin_ban_account,
    "unban":    commands.admin_unban_account,
    "logs":     commands.viewlogs
}
cmdlist["view_profile"] = {
    "view": commands.view_profile
}
cmdlist["update_profile"] = {
    "update_username": commands.update_username,
}
cmdlist["member_bookings"] = {
    "menu": booking.member_frontend,
}
cmdlist["trainer_bookings"] = {
    "generate": booking.generate_next_7_days,
    "editor": booking.trainer_view_and_modify,
    "attendance": booking.attendance,
    "add": booking.add_slots,
    "add_epoch": booking.add_slots_epoch,
}
def online():
    global current_user
    with open(files.ONLINE_PATH, "a") as f:
        f.write(current_user["username"] + "\n")

def offline():
    global current_user
    with open(files.ONLINE_PATH, "r") as f:
        online_users = f.read().splitlines()
    with open(files.ONLINE_PATH, "w") as f:
        for user in online_users:
            if user != current_user["username"]:
                f.write(user + "\n")
def login(users):
    commands.clear()
    try:
        for _ in range(3):
            username = input("Username: ")
            password = getpass.getpass("Password: ") #getpass.getpass() hides password
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
                with open(files.ACCOUNTS_LOG_PATH, "a") as log_file:
                    log_file.write(log_entry)
            except Exception as e:
                print(RED + f"Error logging: {e}" + RESET)
    except KeyboardInterrupt:
        print("Keyboard interrupt. Exiting...")
        exit(0)

    print(RED + "You have exceeded three attempts, please run the program again" + RESET)
    exit(0)

def register(user_data):
    commands.clear()

    try:
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
            "user_type": "Member",
            "uuid": str(uuid.uuid4())
        }

        commands.clear()
        print(f'Username: {username} \nemail: {email}')
        
        confirmed = input("\nRegister? (y/n) ")

    except KeyboardInterrupt:
        print("\n\nRegister cancelled")
        return

    if confirmed.lower() == "y":
        if commands.save_accounts(user_data): #returns False with errors
            print(GREEN + "Registered user, please login again" + RESET)
            time.sleep(2)
        return
    else:
        return

def command_mode():
    # Check if user is banned   
    with open(files.BANNED_PATH, "r") as banned_file:
        banned_users = banned_file.read().splitlines()
    
    if current_user["username"] in banned_users:
        print(RED + f"Your account has been banned, please contact an debug to restate your account" + RESET)
        time.sleep(1)
        exit(0)
    
    online()
    #   Will now act like a shell with commands
    #   Commands are categorized by permissions, examples:
    #   msa admin_delete_account
    #   msa admin_add_account 
    #   msa admin_delete_account john_doe
    #   mma delete_account 
    #   etc.
    #   First word is permission, second word is command, following words are arguments
    #   Some commands wont have arguments
    #   Users are only allowed to run commands, if the permission of the command is in the permissions list

    #I think after we're done with everything, I'll build something like a TUI when the user just types a permission
    user_data = commands.load_accounts()
    if user_data is None:
        exit(1)
    
    permissions = user_data["permissions"].get(current_user["user_type"], [])
    if "debug" in permissions:
        permissions = [
        "admin", 
        "manage_staff_accounts", 
        "manage_member_accounts", 
        "send_comments", 
        "view_comments",
        "view_profile",
        "member_bookings",
        "trainer_bookings",
        ]

    # Admin has all permissions, make sure to add every permission here

    # cmdlist contains permissions, and the permissions are dicts
    # Keys will store command names, values will store function references
    # Printing the values will show where in memory the function is stored, which is probably not safe



    def help():
        for p in permissions:
            print(CYAN + f"{p}: {', '.join(cmdlist[p].keys())}" + RESET)

    mini_cmd_list = {           # This is for commands without arguments.
        "exit": lambda: "EXIT",
        "logout": lambda: "EXIT", # signal loop to return to main menu
        "help": help,
        "h": help,
        "clear": commands.clear # clear console
    }                 

    print("\nType 'h' or 'help' for list of commands within your permission level, 'exit' or CTRL+C to logout and quit.\nYou can do CTRL + C to cancel a command.")
    print(CYAN + f"\nYour permissions: {', '.join(permissions)}" + RESET)

    try:                                # Wrapping the whole thing to catch keyboard interrupts
        while True:
            command = input(f'[{current_user["user_type"]} {current_user["username"]}@Fitness Center] ')
            command = command.strip()   # remove leading and trailing whitespace
            command = command.split()   # splits each word into a list
            if command == []:
                continue

            # Check if user is banned   
            with open(files.BANNED_PATH, "r") as banned_file:
                banned_users = banned_file.read().splitlines()
            
            with open(files.DELETE_PATH, "r") as delete_file:
                deleted_users = delete_file.read().splitlines()

            if current_user["username"] in banned_users:
                print(RED + f"Your account has been banned, please contact an debug to restate your account" + RESET)
                offline()
                time.sleep(1)
                exit(0)
            
            if current_user["username"] in deleted_users:
                print(RED + f"Your account has been deleted, please contact an debug to restate your account" + RESET)
                offline()
                deleted_users.remove(current_user["username"])

                with open(files.DELETE_PATH, "w") as f:
                    f.write("\n".join(deleted_users))
                
                time.sleep(1)
                exit(0)
           
            if len(command) < 2:
                if command[0] == "tui":
                    verbose = True 
                    perm = TUI(BG_MAGENTA + BOLD, "Select permission level", permissions, verbose)

                    if perm is None:
                        continue

                    options = list(cmdlist[perm].keys()) # Since it's a dict, we need to make it subscriptable. 
                    cmd_name = TUI(BG_MAGENTA + BOLD, f"Select command for permission {perm}\n", options, verbose)

                    if cmd_name is None:                 # if user prematurely presses CTRL+C
                        continue

                    args = []
                    func = cmdlist[perm][cmd_name]

                    try:
                        func(current_user, *args)
                    except KeyboardInterrupt:
                        print("\nCancelled")
                    continue

                if command[0] in permissions:
                    verbose = True
                    perm = command[0]
                    options = list(cmdlist[perm].keys()) # Since it's a dict, we need to make it subscriptable. 
                    cmd_name = TUI(BG_MAGENTA + BOLD, f"Select command for permission {perm}\n", options, verbose)

                    if cmd_name is None:                 # if user prematurely presses CTRL+C
                        continue

                    args = []
                    func = cmdlist[perm][cmd_name]
                    
                    try:
                        func(current_user, *args)
                    except KeyboardInterrupt:
                        print("\nCancelled")
                    continue
                
                if command[0] not in mini_cmd_list:
                    print(RED + "Unknown command or invalid format" + RESET)
                    continue
                else:
                    func = mini_cmd_list[command[0]]
                    try:
                        result = func()

                        if result == "EXIT":
                            print("Bye!")
                            offline()
                            time.sleep(1)
                            return
                
                    except KeyboardInterrupt:
                        print("\nCancelled")
                        continue
                
            else:
                perm = command[0]
                cmd_name = command[1]
                args = command[2:] if len(command) > 2 else []
                
                if perm not in permissions:
                    print(RED + "Unknown permission / Access denied" + RESET)
                    continue
                if cmd_name not in cmdlist[perm]:
                    print(RED + "Unknown command" + RESET)
                    continue
                
                func = cmdlist[perm][cmd_name]      # Call the function stored in the dictionary
                try: 
                    func(current_user, *args)
                except KeyboardInterrupt:           # Cancel command with CTRL+C
                    print("\nCancelled")

    except KeyboardInterrupt:
        print("\nBye!")
        offline()

        try:
            time.sleep(1)
        except KeyboardInterrupt:
            return

        return


def main():  # This function will be run first 
    user_data = commands.load_accounts() #returns None with errors
    if user_data is None:
        exit(1)
    
    while True:
        commands.clear()

        options = ["1. Login", "2. Register", "3. Exit"]
        instruction = "Arrow keys to select, Enter to confirm"
        key = TUI(BG_MAGENTA + BOLD, instruction, options, False)
        
        
        '''
        key = input("1. Login \n2. Register \n3. Exit")
        '''
        
        if key == 0: 
            global current_user
            current_user = login(user_data["users"]) #users only, because im not modifying accounts.json
            print(GREEN + f'You are now logged in as {current_user["username"]}, permissions: {current_user["user_type"]}' + RESET)
            command_mode()
        elif key == 1:
            register(user_data) #the entire thing
        elif key == 2:
            exit(0)
        else:
            print(RED + "Invalid input" + RESET)

            try:
                time.sleep(0.2)
            except KeyboardInterrupt:
                return


if __name__ == "__main__":
    main()

#ahhhhh