Usage
#####

Installation 
************
.. code-block:: bash

    git clone https://github.com/pcb1631/PYP
    
Or download the zip file and extract it TO ONE FOLDER AS-IS.

Running the project
*******************
**IDEs will always have issues with input and rendering, so it is reccomended that you use a dedicated terminal like CMD/Powershell or Ghostty.**

.. code-block:: bash

    python main.py
    
OR
    
.. code-block:: bash

    python ./PYP/main.py #the directory of the project
    
Or double click main.py on Windows. Some functionalities are only on Linux but WSL is an option.

But in real world use, it is assumed that the script is in a full screen terminal preventing the user from stopping the script, with whatever means necessary

For example:

In a Linux distro, run this script at startup in a TTY without a display manager. This way it is gurranteed the user never exits the script.

.. code-block:: bash
    
    #!/bin/bash
    
    trap '' SIGINT #ignore CTRL + C interrupt
    
    while true; do
        python main.py
    done





TUI
****
The TUI will be the first thing you encounter in the project.

The first line is the prompt, the lines in the middle are the options, and the last line is fuzzy search. Your selection is the highlighted option

.. figure:: images/TUI.png

    TUI brought up with the command ``admin ban``
    
|
    
Typing will make a query, and uses fuzzy search to change your selection to the closest match.

.. figure:: images/TUI_query.png
    
    Typing ``Rin`` autocompletes to ``Rinzer``
    
|
    
Press arrow keys to change selection and enter to confirm. If the options out number the size of your terminal, the TUI will scroll the options!

Press CTRL+C to cancel at any point



Register
*********
.. explain about registration

Login
******
.. prentend we're logging in as a trainer

CLI
****
Once you're logged in, you'll be met with the following:

.. figure:: images/CLI.png

if you have an active membership, it will show how many days you have left!

.. figure:: images/help.png
    
    typing ``h`` in the CLI
    
|

The blue words are your permissions, the bold words are the commands under that permission, and stuff after the colon are arguments. If an argument has a value assigned, that is the default value.

But you can go ahead and skip the CLI altoghether by typing a permission, or ``tui`` to bring up the TUI.

.. figure:: images/typeperm.png
    
    The TUI after typing the permission ``trainer_bookings``
    
The booking system
*******************
Heavily inspired by iConsult in APSpace, trainers can make time slots for users to book. 

As a Trainer
============
You can simply run ``trainer_bookings`` to bring up the TUI and view all the available commands 

Adding time slots
------------------

To manually add time slots to your booking,


.. code-block:: bash

    trainer_bookings add_slots



Editing and signing attendance
------------------------------

.. code-block:: bash 

   trainer_bookings editor



Generating slots
----------------
If you have decided that the process of adding timeslots is too cumbersome, there is a dedicated command to generate 4 slots for 7 days each.

.. code-block:: bash

    trainer_bookings generate


As a Member
===========



Booking time slots
------------------


As an Admin
===========

Assigning venues to timeslots
-----------------------------

As Frontdesk
============

Signing attendance
------------------




The membership system
**********************

