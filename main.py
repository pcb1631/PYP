#internal libraries
import getpass
import re
import time
import uuid
import inspect

#local project libraries
import commands
from utils import *

from tui import TUI
from colors import *
import files
import booking
import membership
#globals
current_user = {}

def safe_call(func, *args, **kwargs): # *args is for arguments (order matters!), **kwargs is for keyword arguments (order doesn't matter)
    """
    Calls a given function with arbitrary number of arguments. This is what is used when a user runs a command; any raised errors will be caught here.

    :param func: function to call
    :type func: function
    :param args: arguments to pass to function
    :type args: tuple
    :param kwargs: keyword arguments to pass to function (this is probably never used)
    :type kwargs: dict
    :return: return output of function
    :rtype: any
    :raises KeyboardInterrupt: if keyboard interrupt is received
    :raises TypeError: if too many arguments or wrong data types are passed
    :raises Exception: Whatever the called function raises
    """
    try:
        return func(*args, **kwargs)
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt")
        return None
    except Exception as e:
        print(RED + f"Error: {e}" + RESET) # Will catch TypeErrors, e.g. too many arguments or wrong data types
        return None

cmdlist = {}    # This is for commands with arguments.
                # The permission object in accounts.json contains user types, and user types contains the permissions
cmdlist["manage_staff"] = {
    "delete":   commands.admin_delete_account,
    "add":      commands.admin_add_account,
    "edit":     commands.admin_edit_account,
    "view":     commands.admin_view_account
}
cmdlist["manage_members"] = {
    "delete":   commands.fd_delete_account,
    "add":      commands.fd_add_account,
    "edit":     commands.fd_edit_account,
    "topup":    membership.fd_top_up
}

cmdlist["send_comments"] = {
    "comment":  commands.send_comment
}
cmdlist["view_comments"] = {
    "view":     commands.view_comments
}
cmdlist["admin"] = { # There is a user type "admin", and this is a permission called "admin". Keep in mind
    "ban":      commands.admin_ban_account,
    "unban":    commands.admin_unban_account,
    "logs":     commands.viewlogs,
    "texedit":  commands.text_editor
}
cmdlist["profile"] = {
    "view": commands.user_view_account,
    "edit": commands.user_edit_account
}
cmdlist["member_bookings"] = {
    "menu": booking.member_frontend,
}
cmdlist["membership"] = {
    "buy": membership.buy_membership,
    "upgrade": membership.upgrade_membership,
    "cancel": membership.cancel_membership,
    "topup": membership.top_up_balance,
}
cmdlist["my_transactions"] = {
    "view": membership.transaction_history_self,
}
cmdlist["trainer_bookings"] = {
    "generate": booking.generate_next_7_days,
    "editor": booking.trainer_editor,
    "add": booking.add_slots,
    "add_epoch": booking.add_slots_epoch,
}
cmdlist["admin_bookings"] = {
    "assign": booking.venue,
}
cmdlist["attendance"] = {
    "attendance": booking.attendance,
}
cmdlist["transactions"] = {
    "view": membership.transaction_history,
    "report": membership.generate_report,
}



def online():
    """
    Adds the current user to the online file
    """
    global current_user
    write_line(current_user["username"], files.ONLINE_PATH)
    
def offline():
    """
    Removes the current user from the online file. Ignores instances of the same user 
    """
    global current_user
    count = 0
    with open(files.ONLINE_PATH, "r") as f:
        online_users = f.read().splitlines()

    with open(files.ONLINE_PATH, "w") as f:
        for user in online_users:
            if user == '':
                continue
            if user != current_user["username"]:
               f.write("\n" + user)
            else:
                count += 1
                if count > 1:
                    f.write("\n" + user) # do not overwrite instances of the same user



def who():
    """
    Prints all instances of online users
    """
    with open(files.ONLINE_PATH, "r") as f:
        print(f.read().splitlines())

def login(users):
    """
    Logs in a user. Changes current_user global variable after successful login

    :param users: The users object in accounts.json 
    :type users: dict
    """
    commands.clear()
    try:
        for _ in range(3):
            username = input("Username: ")
            password = getpass.getpass("Password: ") #getpass.getpass() hides password
            time.sleep(0.2) #just to make it hard to bruteforce

            if username in users:
                if users[username]["password"] == password: #will crash if I put both in AND
                    print(GREEN + "Welcome to Fitness Center!" + RESET)
                    return {"username": username, "user_type": users[username]["user_type"]}

            print(RED + "Username does not exist or password is incorrect. Please try again" + RESET)


            # Log failed login attempt
            import datetime
            timestamp = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
            log_entry = f"{timestamp} FAILED LOGIN ATTEMPT: {username}"
            write_line(log_entry, files.ACCOUNTS_LOG_PATH)
    except KeyboardInterrupt:
        print("Keyboard interrupt. Exiting...")
        exit(0)

    print(RED + "You have exceeded three attempts, please run the program again" + RESET)
    exit(0)

def register(user_data):
    """
    Registers a new user. Adds the user to accounts.json

    :param user_data: The entirety of accounts.json
    :type user_data: dict
    """
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
            "uuid": str(uuid.uuid4()),
            "balance - RM": 0,
            "membership_tier": None,
            "age": 0,
            "gender": None,
            "phone number": None
        }

        commands.clear()
        print(f'Username: {username} \nemail: {email}')

        confirmed = input("\nRegister? (y/n) ")

    except KeyboardInterrupt:
        print("\n\nRegister cancelled")
        return

    temp = {}
    temp["username"] = None
    if confirmed.lower() == "y":
        save_json(files.ACCOUNTS_PATH, user_data, temp)
        print(GREEN + "Registered user, please login again" + RESET)
        time.sleep(2)
        return
    else:
        return

def command_mode():
    """
    The main command mode loop. Handles user input and calls the appropriate function with safe_call(). Will also check if the user is banned or deleted.
    """
    # Check if user is banned
    with open(files.BANNED_PATH, "r") as banned_file:
        banned_users = banned_file.read().splitlines()

    if current_user["username"] in banned_users:
        print(RED + f"Your account has been banned, please contact an admin to restate your account" + RESET)
        time.sleep(1)
        exit(0)

    user_data = load_json(files.ACCOUNTS_PATH)
    if user_data is None:
        exit(1)
    online()
    tier = user_data["users"][current_user["username"]]["membership_tier"]
    if tier is not None:
        expiry = load_json(files.EXPIRY_PATH)

        if expiry is not None and current_user["username"] in expiry:

            if time.time() > expiry[current_user["username"]]:
                print(RED + "Your membership has expired. Please renew it." + RESET)
                user_data["users"][current_user["username"]]["membership_tier"] = None
                save_json(files.ACCOUNTS_PATH, user_data, current_user)
            else:
                timeleft = expiry[current_user["username"]] - time.time()
                timeleft = timeleft // (24 * 60 * 60) # convert to days
                print(YELLOW + "Time before membership expires: " + str(int(timeleft)) + " days" + RESET)


    permissions = user_data["permissions"].get(current_user["user_type"], [])
    if "debug" in permissions:
        permissions = cmdlist.keys()

    # cmdlist contains permissions, and the permissions are dicts
    # Keys will store command names, values will store function references
    # Printing the values will show where in memory the function is stored, which is probably not safe



    def help():
        for permission in permissions:
            print(CYAN + f"{permission}: " + RESET)
            commands = cmdlist[permission]
            for command in commands:
                print(BOLD + command + RESET, end="")
                param = inspect.signature(commands[command])
                param = str(param)
                param = param[14:-1] # remove the first 14 and last 1 characters
                if param != "":
                    print(": "+param) # prints the signature of the function (what arguments it takes)
                else:
                    print()
            print()
        print("Usage: permission command [args]       (arg order matters!)")
        print("Arguments that already have default values are optional")
        print("Examples of valid commands:")
        print("trainer_bookings add")
        print("trainer_bookings add 2025 12 22 15 42")
        print("trainer_bookings add 2025 12")

    mini_cmd_list = {           # This is for commands without arguments.
        "exit": lambda: "EXIT",
        "logout": lambda: "EXIT", # signal loop to return to main menu
        "help": help,
        "h": help,
        "clear": commands.clear, # clear console
        "who": who
    }

    print("\nType 'h' or 'help' for list of commands within your permission level, 'exit' or CTRL+C to logout and quit.\nYou can do CTRL + C to cancel a command.")
    print(CYAN + f"\nYour permissions: {', '.join(permissions)}" + RESET)

    try:                                # Wrapping the whole thing to catch keyboard interrupts
        while True:
            try:
                command = input(f'[{current_user["user_type"]} {current_user["username"]}@Fitness Center] > ')
            except EOFError:
                print("EOF") # when you go in tui, exit from tui, and then press CTRL+C, this happens.s
                time.sleep(1)
                offline()
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
                print(RED + f"Your account has been banned, please contact an admin to restate your account" + RESET)
                offline()
                time.sleep(1)
                exit(0)

            if current_user["username"] in deleted_users:
                print(RED + f"Your account has been deleted, please contact an admin to restate your account" + RESET)
                offline()
                deleted_users.remove(current_user["username"])

                with open(files.DELETE_PATH, "w") as f:
                    f.write("\n".join(deleted_users))

                time.sleep(1)
                exit(0)

            if len(command) < 2:
                if command[0] == "tui":
                    verbose = True
                    perm = TUI(BG_MAGENTA + BOLD, "Select permission level", list(permissions), verbose)

                    if perm is None:
                        continue

                    options = list(cmdlist[perm].keys()) # Since it's a dict, we need to make it subscriptable.
                    cmd_name = TUI(BG_MAGENTA + BOLD, f"Select command for permission {perm}\n", options, verbose)

                    if cmd_name is None:                 # if user prematurely presses CTRL+C
                        continue

                    args = []
                    func = cmdlist[perm][cmd_name]

                    safe_call(func, current_user, *args)
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

                    safe_call(func, current_user, *args)
                    continue

                if command[0] not in mini_cmd_list:
                    print(RED + "Unknown command or invalid format" + RESET)
                    continue
                else:
                    func = mini_cmd_list[command[0]]
                    result = safe_call(func)

                    if result == "EXIT":
                        print("Bye!")
                        offline()
                        time.sleep(0.2)
                        return

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
                safe_call(func, current_user, *args)

    except KeyboardInterrupt:
        print("\nBye!")
        offline()

        try:
            time.sleep(0.2)
        except KeyboardInterrupt:
            return

        return


def main():  # This function will be run first
    """
    The first function that runs in the script. Handles the login and registration process, and calls command_mode() if login is successful
    """
    try:
        user_data = load_json(files.ACCOUNTS_PATH)
    except Exception as e:
        print(RED + f"Error loading accounts.json: {e}" + RESET)
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
        elif key == None:
            return


if __name__ == "__main__":
    main()

#ahhhhh
