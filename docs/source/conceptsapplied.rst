Programming Concepts Applied
############################
"Include detailed explanations of how Python programming concepts were
implemented, with sample source code from your system"

Application of Storage Types
============================
See: :ref:`Demistifying each file <python-file-explanations>`

Logically, the most prominent data type in the project is dictionaries.

Examples
--------

Dictionaries
~~~~~~~~~~~~

Lists
~~~~~

Text files
~~~~~~~~~~
Ryan's part is a good example



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
    :emphasize-lines: 19-31


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