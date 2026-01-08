Conclusion
==========

Why use De Gym Management System?
---------------------------------
#. Small learning curve
#. Easy config
#. Easy to add new features
#. Multi-instance and live file updates
#. Includes all the essentials for gym management



Limitations
-----------
- The curses module is only packaged with the Linux version of python, so no non-blocking input
    - It's possible to develop non-blocking input for Linux and Windows, but windows and curses syntax is so different that it means we have to write two implementations for any TUI related feature, and that doesn't fit into our timeframe. The curses module was discovered by us during late-development
    
    - This also means we can't develop realtime direct-messaging

Provide example of linux non-blocking input here, which doesn't work currently (not curses) and reference

- nothing preventing users from writing to the same file at once
    - Considering the number of people using the system at once, this wouldnt be a problem most of the time, but a DB would be a better solution

- No features that most shells have (like command history, tab completion, etc.)

- Since we can't import third-party libraries, we can't use encryption or hashing for passwords. And it isn't in our timeframe to implement it. As such passwords are stored in plain text

- The payment system is mostly cosmetic

How can De Gym Management System be improved?
---------------------------------------------
Fortunately because of the scalability and modularity of the project, it is almost trivial to add new features.

See: :ref:`Adding new commands and features <adding-commands>`

Features to add
~~~~~~~~~~~~~~~

- Banking or Touch n Go API
- encryption for accounts.json
- piping I/O
- database
- grep, tab completion, etc. (shell features)
- the curses module
- ...or any third-party library