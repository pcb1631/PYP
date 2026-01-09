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
- encryption for passwords
- common shell features
    - piping I/O
    - grep
    - tab completion
    - command history
- database
- live messaging
- ...or any third-party library

One caveat: Windows has command history, that is a result of powershell's/CMD's behaviour and is not implemented by us