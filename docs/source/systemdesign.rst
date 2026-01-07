System design
##############

Permission and command structure
---------------------------------

See: :ref:`config` 

Graph this!

``command_mode (get user's permissions) ==> accounts.json``

``command_mode (get commands under said permissions) ==> cmdlist``

.. _error_flow:

Data, file handling, and error handling flow
---------------------------------------------

Graph this!

``main.py (user types in command) ==> commands.py, membership.py, booking.py (use utils.py for file handling) ==> utils.py``

``utils.py (load_json or save_json raises exception) ==> commands.py, membership.py, booking.py (halted by raised exception from utils.py, or raises its own exception) ==> main.py (safe_call catches the error)``