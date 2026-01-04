Demystifying each file
======================
This section will fully explain (if not trivial) each file in the project. The subsections represent folders, and the sub-subsections represents the files itself.

logs
----
The logs folder holds .log files than contain user history. Potential debugging, or finding culprits to certain problems. The .log suffix is completely arbitrary and can be parsed or formatted in any way. 

accounts.log
~~~~~~~~~~~~

comments.log
~~~~~~~~~~~~

transactions.log
~~~~~~~~~~~~~~~~

userData
--------
Persistent user data. Any changes made here will be reflected in the system

accounts.json
~~~~~~~~~~~~~
accounts.json contains two main objects, **permissions** and **users**. Permissions is made for configuration by admins.

bookings.json
~~~~~~~~~~~~~

expiry.json
~~~~~~~~~~~
When a user buys or upgrades a membership, their username will be added here as a key, with the value being the month after they bought the membership. (In UNIX timestamp)

concurrent
----------

delete
~~~~~~

online
~~~~~~

In the project folder itself
----------------------------

banned
~~~~~~

.. _python-file-explanations:

booking.py
~~~~~~~~~~
.. code-block:: python
    :caption: imports for bookings.py
    :linenos:
    
    import json 
    from tui import TUI, timeTUI # local library
    import time 
    from datetime import datetime 
    from utils import * # local library
    from colors import * #local library
    import files
   
    
.. autofunction:: booking.sort_slots

.. code-block:: python
    :lineno-start: 16

    def sort_slots(trainer):
    bookings = load_json(files.BOOKING_PATH)
    slots = []
    for slot in bookings[trainer]:
        slots.append(bookings[trainer][slot])
    slots.sort(key=lambda x: x["start"]) # sort with regards to start time

    bookings[trainer] = {} # clear slots

16. Takes trainer’s name as input. 

#. Loads the data from BOOKING_PATH and saves as ``bookings``. 

#. Creates an empty list named ``slots``. 

#. Loops through each slot from a specific trainer. 

#. Adds the trainer’s available slots into ``slots``. 

#. Sorts the slots in the list based on the start time. 

23. clears slots in ``bookings[trainer]``

.. code-block:: python
    :lineno-start: 24

    for i in range(len(slots)): 
        bookings[trainer][str(i)] = slots[i] 
    current_user = { "username": trainer, "user_type": "Trainer" } 
    save_json(files.BOOKING_PATH, bookings, current_user) 

24. Loops through the sorted slots via i index.. 

#. Enters new reordered slots back into “slots”. 

#. Creates dictionary called “current_user” that saves the “username” and “user_type”. 

#. Saves the new data into the JSON file. 

.. autofunction:: booking.generate_next_7_days

.. autofunction:: booking.add_slots

.. autofunction:: booking.trainer_editor

.. autofunction:: booking.add_slots_epoch

.. autofunction:: booking.attendance

.. autofunction:: booking.venue

.. autofunction:: booking.member_frontend

colors.py
~~~~~~~~~

main.py
~~~~~~~

.. autofunction:: main.main

.. autofunction:: main.safe_call

.. autofunction:: main.online

.. autofunction:: main.offline

.. autofunction:: main.who

.. autofunction:: main.login

.. autofunction:: main.register

.. autofunction:: main.command_mode

commands.py
~~~~~~~~~~~

.. autofunction:: commands.clear

.. autofunction:: commands.admin_delete_account

.. autofunction:: commands.admin_add_account

.. autofunction:: commands.admin_edit_account

.. autofunction:: commands.fd_delete_account

.. autofunction:: commands.fd_add_account

.. autofunction:: commands.fd_edit_account

.. autofunction:: commands.user_edit_account

.. autofunction:: commands.admin_view_account

.. autofunction:: commands.user_view_account

.. autofunction:: commands.admin_ban_account

.. autofunction:: commands.admin_unban_account

.. autofunction:: commands.direct_messages

.. autofunction:: commands.send_comment

.. autofunction:: commands.view_comments

.. autofunction:: commands.viewlogs

.. autofunction:: commands.text_editor

files.py
~~~~~~~~
Contains cross-os file path constants for each non-python file

.. code-block:: python
    :caption: imports for files.py

    import os


.. autofunction:: files.path

.. code-block:: python
    :lineno-start: 2 

    #File paths, will be relative to this files.py file and is compatible with all os
    
    def path(*args):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

Explanation for above

|

Further contents of the file:
        
.. code-block:: python
    :lineno-start: 7

    # examples:
    # FILE_PATH = path("folder1", "folder2", "file")
    # FILE_PATH = path("file")
    
    ACCOUNTS_PATH       = path("userData", "accounts.json")   #userdata/accounts.json
    ACCOUNTS_LOG_PATH   = path("logs", "accounts.log")    #logs/accounts.log
    CHECKIN_LOG_PATH    = path("logs", "checkin.log")      #logs/checkin.log
    MESSAGES_LOG_PATH   = path("logs", "messages.log")    #logs/messages.log
    COMMENTS_LOG_PATH   = path("logs", "comments.log")
    BANNED_PATH         = path("banned") 
    BOOKING_PATH        = path("userData", "booking.json")
    ONLINE_PATH         = path("concurrent", "online")
    DELETE_PATH         = path("concurrent", "delete")
    ATTENDANCE_PATH     = path("logs", "attendance.log")
    TRANSACTION_PATH    = path("logs", "transactions.log")
    EXPIRY_PATH         = path("userData", "expiry.json")
    

kb.py
~~~~~

.. autofunction:: kb.get_key

membership.py
~~~~~~~~~~~~~

.. autofunction:: membership.transaction_history_self

.. autofunction:: membership.transaction_history

.. autofunction:: membership.buy_membership

.. autofunction:: membership.upgrade_membership

.. autofunction:: membership.cancel_membership

.. autofunction:: membership.top_up_balance

.. autofunction:: membership.fd_top_up

.. autofunction:: membership.generate_report

tui.py
~~~~~~

.. autofunction:: tui.clear

.. autofunction:: tui.TUI

.. autofunction:: tui.timeTUI

utils.py
~~~~~~~~

.. autofunction:: utils.find

.. autofunction:: utils.epoch_to_readable

.. autofunction:: utils.conflict

.. autofunction:: utils.write_line

.. autofunction:: utils.load_json

.. autofunction:: utils.save_json
