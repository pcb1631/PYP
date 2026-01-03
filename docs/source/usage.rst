Usage
=====

- Cloned with git or extracted from an archive to one folder 

- THE PROJECT MUST BE DOWNLOADED AS-IS 

- Preferably not running in an IDE 

- Running on a Linux distribution, Windows 11, or macOS 
    - Using WSL is reccomended if you're on windows

- Executed with the command “python main.py,” “python ~/Fitness Center/main.py” or similar 

- In a full screen terminal preventing the user from stopping the script, with whatever means necessary (e.g., using a while loop and the trap command (to ignore keyboard interrupts) in a bash script, where the bash script is run on startup in a TTY without a desktop environment) 

Installation 
------------
.. code-block:: bash

    git clone https://github.com/pcb1631/PYP
    
Or download the zip file and extract it TO ONE FOLDER AS-IS.

Running the project
-------------------
.. code-block:: bash

    python main.py
    
OR
    
.. code-block:: bash

    python ./PYP/main.py #the directory of the project
    
Or double click main.py on Windows.

TUI
---
The TUI will be the first thing you encounter in the project.

The first line is the prompt, the lines in the middle are the options, and the last line is fuzzy search. Your selection is the highlighted option 

Press arrow keys to change selection and enter to confirm

Typing will make a query, and uses fuzzy search to change your selection to the closest match.

Press CTRL+C to cancel

Register
--------

Login
-----

CLI
---

