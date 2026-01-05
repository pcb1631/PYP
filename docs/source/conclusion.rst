Conclusion
==========

Why use De Gym Management System?
---------------------------------

Limitations
-----------
- The curses module is only packaged with the Linux version of python, so no non-blocking input
    - It's possible to develop non-blocking input for Linux and Windows, but it means we have to write two implementations for any TUI related feature, and that doesn't fit into our timeframe. The curses module was discovered by us during late-development
    
    - This also means we can't develop realtime direct-messaging

Provide example of linux non-blocking input here, which doesn't work currently (not curses) and reference

- nothing preventing users from writing to the same file at once

- No features that most shells have (like command history, tab completion, etc.)

How can De Gym Management System be improved?
---------------------------------------------
Fortunately because of the scalability and modularity of the project, it is almost trivial to add new features.

Features to add
~~~~~~~~~~~~~~~

- piping I/O
- database
- grep
- the curses module
- ...or any third-party library