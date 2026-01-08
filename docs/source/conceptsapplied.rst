Programming Concepts Applied
############################
"Include detailed explanations of how Python programming concepts were
implemented, with sample source code from your system"

Application of Storage Types
============================
See: :ref:`Demistifying each file <python-file-explanations>`

Logically, the most prominent data type in the project is dictionaries.

:ref:`systemdesign` shows how dicts, lists, and json files act as a system to make permissions work. 

Specific examples
------------------
Dicts and text files
~~~~~~~~~~~~~~~~~~~~
In main.py, there is a global dict current_user, which is passed into functions that involve file handling (e.g. ``utils.save_json``). The functions will only write to files if the current user isn't banned. 

Please see :ref:`multi_instance`


.. code-block:: python
    :caption: the global dict in main.py
    :lineno-start: 17
    
    #globals
    current_user = {}
    
.. code-block:: python
    :caption: main.login
    :lineno-start: 157
    
    if username in users:
        if users[username]["password"] == password: #will crash if I put both in AND
            print(GREEN + "Welcome to Fitness Center!" + RESET)
            return {"username": username, "user_type": users[username]["user_type"]}

.. code-block:: python
    :caption: main.main
    :lineno-start: 447
    :emphasize-lines: 19-21
    
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

.. code-block:: python 
    :caption: utils.save_json
    :lineno-start: 99
    :emphasize-lines: 13-16
    
    def save_json(filepath, data, current_user): # generic json saver
        """
        Saves data to json file 
    
        :param str filepath: The file path
        :param dict data: The data to save
        :param dict current_user: The current user
        :raises PermissionError: if the user is banned or deleted
        :raises Exception: if an error occurs
        """
        username = current_user["username"]
        
        if find(username, files.BANNED_PATH):
            raise PermissionError("You are banned")
        if find(username, files.DELETE_PATH):
            raise PermissionError("Your account has been deleted")
        
        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            raise Exception(f"Error saving to {filepath}: {e}")


Text files
~~~~~~~~~~

Lists
~~~~~

Application of Control Structures:
==================================
trainer_editor


Application of Error Handling
==================================

See: :ref:`error_flow` for how exceptions are caught

.. code-block::
    :caption: Example in membership.top_up_balance
    :lineno-start: 110
    
    try:
        if amount is None:
            amount = float(input("Enter top up amount (RM): "))
        else:
            amount = float(amount)

        if amount < 0:
            raise ValueError("Invalid amount. Please enter a positive amount.")
    except ValueError as e:
        raise e             # This will catch Type errors




Application of Input Validation
==================================

.. code-block:: python 
    :lineno-start: 468
    :caption: commands.admin_ban_account
    :emphasize-lines: 19-30


    user_data = load_json(files.ACCOUNTS_PATH)

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
        write_line(username, files.BANNED_PATH)

        #log the ban
        timestamp = epoch_to_readable(time.time())
        log_entry = f"{timestamp} ACCOUNT: {username} BANNED BY: {current_user['username']}"
        write_line(log_entry, files.ACCOUNTS_LOG_PATH)
        

        print(GREEN + f"Account '{username}' banned successfully." + RESET)

Function Flow Explanations
==================================
See: :ref:`Demistifying each file <python-file-explanations>`